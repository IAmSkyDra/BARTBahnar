from utils.classification import analyze_sentence_with_model
def translate(sentence, solr_url):
    test_sentence = sentence
    # Phân tích câu
    non_foreign_words, remaining_sentence = analyze_sentence_with_model(test_sentence, vietnamese_dict)

    # In kết quả
    print(f"Các từ không phải ngôn ngữ khác: {non_foreign_words}")
    print(f"Câu còn lại (đã đánh dấu): {remaining_sentence}")

    segmented_text = segment_with_phrases(remaining_sentence, phrase_dict)
    # segmented_text = splitSentenceIntoWords(remaining_sentence)
    print("Segmented Sentence:", segmented_text)
    words = normalize_words(segmented_text)
    print(words)

    # Bước 2: Xử lý câu theo batch
    print("Processing input sentence...")

    processed_results = processSentenceBatch(words, f'{solr_url}/select?indent=true&q.op=OR&q=')
    print(processed_results)

    # Bước 3: Ghép lại câu
    output_sentence = reconstructSentenceBatch(processed_results, non_foreign_words)
    print("Processed Sentence:", output_sentence)
    return output_sentence
