from collections import Counter, defaultdict
import math
import re

def load_corpus(file_path):
    """
    Đọc file văn bản, mỗi dòng là một câu,
    trả về danh sách các câu (loại bỏ dòng trống).
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def build_phrase_dict(corpus, max_ngram=5, min_freq=2, min_pmi=3):
    """
    Xây dựng từ điển cụm từ dựa trên chỉ số PMI, sử dụng tổng số n-gram:

    - max_ngram: Độ dài tối đa của cụm (2 -> max_ngram).
    - min_freq: Tần suất tối thiểu để cụm được xét.
    - min_pmi: Ngưỡng PMI tối thiểu để cụm được chọn.

    Công thức PMI (dạng log2):
      PMI(w1, ..., wn) = log2( p(w1,...,wn) / ( p(w1)*...*p(wn) ) )

    Trong đó:
      p(w1,...,wn) = count_ngram / total_ngrams[n]   (xác suất n-gram bậc n)
      p(wi)        = count_unigram / total_ngrams[1] (xác suất unigram)
    """
    # Đếm n-gram và tổng số n-gram
    ngram_counts = defaultdict(Counter)  # n -> Counter( (w1,...,wn) -> count )
    total_ngrams = defaultdict(int)      # n -> tổng số n-gram cấp n
    word_counts = Counter()              # Đếm tần suất unigram

    # 1) Duyệt từng câu trong corpus
    for sentence in corpus:
        # Tách từ, chỉ lấy chữ + số (nếu có)
        words = re.findall(r'\w+', sentence.lower())
        # Đếm unigram
        word_counts.update(words)

        # Đếm n-gram 1..max_ngram
        length = len(words)
        for n in range(1, max_ngram + 1):
            if length >= n:
                # Tạo n-gram bằng zip trượt
                ngrams_in_sentence = zip(*(words[i:] for i in range(n)))
                ngram_list = list(ngrams_in_sentence)
                # Cập nhật
                ngram_counts[n].update(ngram_list)
                total_ngrams[n] += (length - n + 1)

    phrase_dict = {}

    # 2) Tính PMI cho n-gram từ n=2..max_ngram
    for n in range(2, max_ngram + 1):
        for ngram_tuple, ngram_count in ngram_counts[n].items():
            # Kiểm tra tần suất tối thiểu
            if ngram_count < min_freq:
                continue

            # Xác suất n-gram
            p_ngram = ngram_count / total_ngrams[n]

            # Xác suất độc lập (tích xác suất unigram)
            p_indep = 1.0
            for w in ngram_tuple:
                p_w = word_counts[w] / total_ngrams[1]
                p_indep *= p_w

            # Tránh chia 0
            if p_indep <= 0:
                continue

            # Tính PMI
            pmi = math.log2(p_ngram / p_indep)

            # Chọn cụm nếu PMI >= min_pmi
            if pmi >= min_pmi:
                phrase_text = " ".join(ngram_tuple)
                phrase_join = "_".join(ngram_tuple)
                phrase_dict[phrase_text] = phrase_join

    return phrase_dict

def segment_with_phrases(sentence, phrase_dict):
    """
    Thay thế (segment) các cụm từ đã phát hiện trong 'phrase_dict'
    bằng dạng gắn kết (dùng dấu gạch dưới).

    - Ưu tiên thay thế cụm dài nhất (tính theo số ký tự) trước
      để tránh việc cụm ngắn “ăn” cụm dài.
    - Trả về list tokens sau khi thay thế.
    """
    # Đưa về lowercase
    sentence_lower = sentence.lower()

    # Sắp xếp phrase_dict theo độ dài key giảm dần (số ký tự)
    for phrase, replacement in sorted(phrase_dict.items(), key=lambda x: -len(x[0])):
        # Escape phrase để tránh lỗi regex nếu có ký tự đặc biệt
        pattern = rf"\b{re.escape(phrase)}\b"
        sentence_lower = re.sub(pattern, replacement, sentence_lower)

    # Tách theo khoảng trắng để trả về list
    return sentence_lower.split()

if __name__ == "__main__":
    # Ví dụ: Đọc corpus từ file (mỗi dòng một câu)
    corpus_file = "/content/bana_data.txt"
    corpus = load_corpus(corpus_file)

    # Tham số tùy chỉnh
    max_ngram = 3    # Độ dài tối đa của cụm
    min_freq = 2     # Tần suất tối thiểu
    min_pmi = 5      # Ngưỡng PMI tối thiểu (có thể thử 3->7, tuỳ data)

    # Xây dựng từ điển cụm
    phrase_dict = build_phrase_dict(
        corpus,
        max_ngram=max_ngram,
        min_freq=min_freq,
        min_pmi=min_pmi
    )
    print("=== Phrase Dictionary ===")
    for i, (k, v) in enumerate(list(phrase_dict.items())[:10]):
        print(f"{k} -> {v}")
    print("...")

    # Thử nghiệm tách cụm cho một câu
    test_sentence = (
        "'Bang nghiêm thu, 'bang thanh li hơp đông păng 'bang kuyêt toan đei yuêt dĭ kơpal đâu tư adrĭng khôi lươ̆ng tơgǔm pơm chơ đêh têh bal, keh kong tơdrong trong xe, thuy lơi nôi đông, tơdrong ǔnh rang tơgǔm choh jang nông nghiêp"
    )

    segmented_text = segment_with_phrases(test_sentence, phrase_dict)
    print("\n=== Segmented Sentence ===")
    print(segmented_text)