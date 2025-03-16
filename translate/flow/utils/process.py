def processSentenceBatch(words, solr_url):
    """
    Xử lý mảng các từ để tìm các từ cần dịch, tìm kiếm Solr và dịch các từ không tìm thấy.
    """
    search_results = search(words, solr_url)  # Tìm kiếm Solr cho tất cả các từ
    print("Kết quả tìm kiếm từ điển:", search_results)

    sentence = ''
    processed_results = []  # Dùng mảng để lưu kết quả xử lý
    i = 0
    non_dict_words = []  # Lưu các từ không có trong từ điển

    while i < len(words):
        word = words[i]

        # Nếu là từ có dạng <word>, dịch các từ không có trong từ điển trước và giữ nguyên từ <word>
        if word.startswith('<') and word.endswith('>'):
            print(non_dict_words)
            if non_dict_words:
                temp_combined = ' '.join(non_dict_words)  # Gom tất cả các từ không có trong từ điển
                temp_translation = translator.translate(temp_combined.strip())
                print(f"{temp_combined.strip()} -> dịch bằng model: {temp_translation}")

                processed_results.append(temp_translation)
                sentence += temp_translation + ' '
                non_dict_words = []  # Reset danh sách các từ không có trong từ điển sau khi dịch

            processed_results.append(word)
            sentence += word + ' '
            print(f"{word} -> giữ nguyên")
            i += 1
            continue

        best_candidate = None
        best_match_length = 0
        best_combined_word = None

        # Tìm cụm từ dài nhất có thể tìm thấy trong từ điển (từ 1 đến 4 từ)
        for j in range(i, min(i + 4, len(words))):
            combined_word = ' '.join(words[i:j + 1])
            # print(f"Đang kiểm tra cụm từ: {combined_word}")
            candidates = findRelatedCandidates(combined_word, search_results)

            if candidates:
                best_candidate = chooseBestCandidate(sentence, combined_word, candidates)
                best_match_length = j - i + 1  # Độ dài cụm từ khớp tốt nhất
                best_combined_word = combined_word

        # Nếu có best_candidate, dịch các từ không có trong từ điển trước
        if best_candidate:
            print(non_dict_words)
            if non_dict_words:
                temp_combined = ' '.join(non_dict_words)  # Gom tất cả các từ không có trong từ điển
                temp_translation = translator.translate(temp_combined.strip())
                print(f"{temp_combined.strip()} -> dịch bằng model: {temp_translation}")

                processed_results.append(temp_translation)
                sentence += temp_translation + ' '
                non_dict_words = []  # Reset danh sách các từ không có trong từ điển sau khi dịch

            print(f"{best_combined_word} -> dịch bằng từ điển: {best_candidate}")
            processed_results.append(best_candidate)
            sentence += best_candidate + ' '
            i += best_match_length  # Nhảy qua số từ đã ghép

        else:
            # Lưu các từ không có trong từ điển vào danh sách non_dict_words
            non_dict_words.append(word)
            i += 1

    # Nếu còn từ không có trong từ điển, dịch chúng sau khi kết thúc
    if non_dict_words:
        print(non_dict_words)
        temp_combined = ' '.join(non_dict_words)  # Gom tất cả các từ không có trong từ điển
        temp_translation = translator.translate(temp_combined.strip())
        print(f"{temp_combined.strip()} -> dịch bằng model: {temp_translation}")

        processed_results.append(temp_translation)
        sentence += temp_translation + ' '

    return processed_results

from difflib import SequenceMatcher

def similarity_ratio(a, b):
    """
    Tính toán độ tương đồng giữa hai chuỗi a và b, trả về tỷ lệ giống nhau (từ 0 đến 1).
    """
    a = a.replace('_', ' ')  # Loại bỏ dấu gạch dưới
    b = b.replace('_', ' ')  # Loại bỏ dấu gạch dưới
    return SequenceMatcher(None, a, b).ratio()

def findRelatedCandidates(word, search_results):
    """
    Tìm các cụm từ liên quan nếu từ không có trong Solr.
    Kiểm tra nếu word giống bahnar_phrase tới 80% thì nối với nhau.
    """
    related_candidates = []
    for result in search_results:
        if 'bahnar' in result and 'vietnamese' in result:
            bahnar_phrase = result['bahnar']
            vietnamese_candidates = result['vietnamese']

            # Kiểm tra nếu từ cần tìm khớp chính xác với một trong các từ trong bahnar_phrase
            similarity = similarity_ratio(word, bahnar_phrase)
            if similarity >= 0.85:  # Nếu độ tương đồng từ 80% trở lên
                related_candidates.extend(vietnamese_candidates)

    return related_candidates
