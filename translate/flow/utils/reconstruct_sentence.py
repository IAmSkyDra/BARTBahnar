def reconstructSentenceBatch(processed_results, non_foreign_words):
    """
    Ghép lại câu từ các từ đã xử lý, giữ nguyên thứ tự.
    Thay thế các từ có dạng <word> bằng các từ trong non_foreign_words.
    Viết hoa đầu câu và sau dấu chấm, và giữ lại các từ đã dịch đúng cách.
    """
    reconstructed_sentence = []
    non_foreign_index = 0
    capitalize_next = True  # Cờ để xác định khi nào viết hoa

    # Ghép lại câu từ processed_results và non_foreign_words theo thứ tự
    for word in processed_results:
        # Nếu từ là <word>, thay thế bằng từ trong non_foreign_words
        if word == '<word>':
            if non_foreign_index < len(non_foreign_words):
                reconstructed_sentence.append(non_foreign_words[non_foreign_index])
                non_foreign_index += 1
            else:
                reconstructed_sentence.append(word)
        else:
            # Kiểm tra và viết hoa nếu là đầu câu
            if capitalize_next:
                reconstructed_sentence.append(word.capitalize())  # Viết hoa đầu câu
                capitalize_next = False  # Sau khi viết hoa đầu câu, chuyển sang chữ thường
            else:
                reconstructed_sentence.append(word.lower())  # Chuyển các từ còn lại thành chữ thường

        # Cập nhật cờ capitalize_next nếu từ là dấu chấm
        if word.endswith('.'):
            capitalize_next = True

    # Ghép lại câu thành một chuỗi
    reconstructed_sentence = " ".join(reconstructed_sentence).strip()

    # Viết hoa đầu câu nếu cần và thêm dấu chấm cuối câu
    if reconstructed_sentence:
        if not reconstructed_sentence[0].isupper():
            reconstructed_sentence = reconstructed_sentence[0].capitalize() + reconstructed_sentence[1:]
        if not reconstructed_sentence.endswith('.'):
            reconstructed_sentence += '.'

    return reconstructed_sentence