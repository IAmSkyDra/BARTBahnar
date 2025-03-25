from utils.classification import VietnameseTextAnalyzer
from utils.reconstruct_sentence import reconstructSentenceBatch
from utils.segmentword import TextSegmenter
from utils.translator import Translate_Model
from utils.search import SearchTranslator
from utils.best_candidate import BestCandidateSelector
from difflib import SequenceMatcher
from config import WORD_PATH

class Translator:
    """Lớp dịch câu với các bước phân tích, xử lý và ghép lại."""
    
    def __init__(self, classification_model, translator_model, selector_model, solr_url):
        """
        Khởi tạo Translator.
        """
        self.analyzer = VietnameseTextAnalyzer(word_path=WORD_PATH, model_name=classification_model) 
        self.text_segmenter = TextSegmenter()
        
        self.solr_url = solr_url
        self.search_translator = SearchTranslator(solr_url)
        
        # Khởi tạo một đối tượng Translator, mô hình được tải chỉ một lần
        self.translator = Translate_Model(translator_model)
        self.selector = BestCandidateSelector(selector_model)


    def translate(self, sentence):
        test_sentence = sentence
        # Phân tích câu
        non_foreign_words, remaining_sentence = self.analyzer.analyze_sentence(test_sentence)

        # In kết quả
        # print(f"Các từ không phải ngôn ngữ khác: {non_foreign_words}")
        # print(f"Câu còn lại (đã đánh dấu): {remaining_sentence}")

        segmented_text = self.text_segmenter.segment(remaining_sentence)
        # segmented_text = splitSentenceIntoWords(remaining_sentence)
        # print("Segmented Sentence:", segmented_text)
        words = self.analyzer.normalize_words(segmented_text)
        # print(words)

        # Bước 2: Xử lý câu theo batch
        # print("Processing input sentence...")

        processed_results = self.processSentenceBatch(words, f'{self.solr_url}/select?indent=true&q.op=OR&q=')
        # print(processed_results)

        # Bước 3: Ghép lại câu
        output_sentence = reconstructSentenceBatch(processed_results, non_foreign_words)
        # print("Processed Sentence:", output_sentence)
        return output_sentence
    
    
    def processSentenceBatch(self, words, solr_url):
        """
        Xử lý mảng các từ để tìm các từ cần dịch, tìm kiếm Solr và dịch các từ không tìm thấy.
        """
        search_results = self.search_translator.search(words)  # Tìm kiếm Solr cho tất cả các từ
        # print("Kết quả tìm kiếm từ điển:", search_results)

        sentence = ''
        processed_results = []  # Dùng mảng để lưu kết quả xử lý
        i = 0
        non_dict_words = []  # Lưu các từ không có trong từ điển

        while i < len(words):
            word = words[i]

            # Nếu là từ có dạng <word>, dịch các từ không có trong từ điển trước và giữ nguyên từ <word>
            if word.startswith('<') and word.endswith('>'):
                # print(non_dict_words)
                if non_dict_words:
                    temp_combined = ' '.join(non_dict_words)  # Gom tất cả các từ không có trong từ điển
                    temp_translation = self.translator.translate(temp_combined.strip())
                    # print(f"{temp_combined.strip()} -> dịch bằng model: {temp_translation}")

                    processed_results.append(temp_translation)
                    sentence += temp_translation + ' '
                    non_dict_words = []  # Reset danh sách các từ không có trong từ điển sau khi dịch

                processed_results.append(word)
                sentence += word + ' '
                # print(f"{word} -> giữ nguyên")
                i += 1
                continue

            best_candidate = None
            best_match_length = 0
            best_combined_word = None

            # Tìm cụm từ dài nhất có thể tìm thấy trong từ điển (từ 1 đến 4 từ)
            for j in range(i, min(i + 4, len(words))):
                combined_word = ' '.join(words[i:j + 1])
                # print(f"Đang kiểm tra cụm từ: {combined_word}")
                candidates = self.findRelatedCandidates(combined_word, search_results)

                if candidates:
                    best_candidate = self.selector.choose_best_candidate(sentence, candidates)
                    best_match_length = j - i + 1  # Độ dài cụm từ khớp tốt nhất
                    best_combined_word = combined_word

            # Nếu có best_candidate, dịch các từ không có trong từ điển trước
            if best_candidate:
                # print(non_dict_words)
                if non_dict_words:
                    temp_combined = ' '.join(non_dict_words)  # Gom tất cả các từ không có trong từ điển
                    temp_translation = self.translator.translate(temp_combined.strip())
                    # print(f"{temp_combined.strip()} -> dịch bằng model: {temp_translation}")

                    processed_results.append(temp_translation)
                    sentence += temp_translation + ' '
                    non_dict_words = []  # Reset danh sách các từ không có trong từ điển sau khi dịch

                # print(f"{best_combined_word} -> dịch bằng từ điển: {best_candidate}")
                processed_results.append(best_candidate)
                sentence += best_candidate + ' '
                i += best_match_length  # Nhảy qua số từ đã ghép

            else:
                # Lưu các từ không có trong từ điển vào danh sách non_dict_words
                non_dict_words.append(word)
                i += 1

        # Nếu còn từ không có trong từ điển, dịch chúng sau khi kết thúc
        if non_dict_words:
            # print(non_dict_words)
            temp_combined = ' '.join(non_dict_words)  # Gom tất cả các từ không có trong từ điển
            temp_translation = self.translator.translate(temp_combined.strip())
            # print(f"{temp_combined.strip()} -> dịch bằng model: {temp_translation}")

            processed_results.append(temp_translation)
            sentence += temp_translation + ' '

        return processed_results

    def similarity_ratio(self, a, b):
        """
        Tính toán độ tương đồng giữa hai chuỗi a và b, trả về tỷ lệ giống nhau (từ 0 đến 1).
        """
        a = a.replace('_', ' ')  # Loại bỏ dấu gạch dưới
        b = b.replace('_', ' ')  # Loại bỏ dấu gạch dưới
        return SequenceMatcher(None, a, b).ratio()

    def findRelatedCandidates(self, word, search_results):
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
                similarity = self.similarity_ratio(word, bahnar_phrase)
                if similarity >= 0.85:  # Nếu độ tương đồng từ 80% trở lên
                    related_candidates.extend(vietnamese_candidates)

        return related_candidates

