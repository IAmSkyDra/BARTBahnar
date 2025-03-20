import spacy
import re
import requests
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import os

class VietnameseTextAnalyzer:
    def __init__(self, word_path=None, model_name="undertheseanlp/vietnamese-ner-v1.4.0a2", dictionary_folder="data"):
        """
        Khởi tạo mô hình với từ điển và mô hình NER.
        """
        self.vietnamese_dict = self.load_vietnamese_dictionary(word_path)

        # Tạo mô hình spaCy cho tiếng Việt
        self.nlp_spacy = spacy.blank("vi")

        # Tải mô hình NER
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.ner_model = pipeline("ner", model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")
        
    def download_vietnamese_dictionary(self, url, file_path):
        """
        Tải từ điển tiếng Việt từ Google Sheets (exported as XLSX).
        """
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            # print(f"Từ điển đã được tải và lưu tại: {file_path}")
        else:
            print(f"Không thể tải từ điển. Mã lỗi: {response.status_code}")

    def load_vietnamese_dictionary(self, file_path):
        """
        Tải từ điển tiếng Việt từ file Excel.
        """
        df = pd.read_csv(file_path, usecols=[0], header=None)
        return set(df[0].str.strip().str.lower().dropna())


    def is_special_character(self, word):
        """
        Kiểm tra nếu từ chứa ký tự đặc biệt.
        """
        return bool(re.match(r"[#$%&()*+,-./:;<=>?@\[\]^`{}~]", word))

    def is_number(self, word):
        """
        Kiểm tra nếu từ là số hoặc có dạng số thực.
        """
        return word.isdigit() or bool(re.match(r"^0*\d+(\.\d+)?$", word))

    def is_date(self, word):
        """
        Kiểm tra nếu từ có dạng ngày tháng năm.
        """
        date_formats = [
            r"^\d{1,2}/\d{1,2}/\d{4}$",  # dd/mm/yyyy
            r"^\d{1,2}-\d{1,2}-\d{4}$",  # dd-mm-yyyy
            r"^\d{4}/\d{1,2}/\d{1,2}$",  # yyyy/mm/dd
            r"^\d{4}-\d{1,2}-\d{1,2}$",  # yyyy-mm-dd
        ]
        return any(re.match(date_format, word) for date_format in date_formats)

    def is_vietnamese_word(self, word):
        """
        Kiểm tra nếu từ thuộc từ điển tiếng Việt.
        """
        return word.lower() in self.vietnamese_dict

    def analyze_sentence(self, sentence):
        """
        Phân tích câu, phân loại từng từ và giữ lại phần không phải ngôn ngữ khác.
        """
        # Tokenize câu bằng spaCy
        doc = self.nlp_spacy(sentence)
        tokens = [token.text for token in doc]

        results = []
        for word in tokens:
            if self.is_special_character(word):
                results.append((word, "Ký tự đặc biệt"))
            elif self.is_number(word):
                results.append((word, "Số"))
            elif self.is_date(word):
                results.append((word, "Ngày tháng năm"))
            elif self.is_vietnamese_word(word):
                results.append((word, "Tiếng Việt"))
            else:
                results.append((word, "Ngôn ngữ khác"))

        # Giữ lại các từ không phải ngôn ngữ khác
        non_foreign_words = [word for word, category in results if category != "Ngôn ngữ khác"]

        # Tạo câu còn lại với các phần không phải ngôn ngữ khác
        remaining_sentence = " ".join([f"<word>" if category != "Ngôn ngữ khác" else word
                                       for word, category in results])

        return non_foreign_words, remaining_sentence

    def normalize_words(self, word_list):
        """
        Chuẩn hóa danh sách từ (loại bỏ dấu gạch dưới và chuyển thành chữ thường).
        """
        return [word.replace('_', ' ').lower() for word in word_list]


# ========================== CÁCH SỬ DỤNG ==========================
# if __name__ == "__main__":
#     # Link tải từ điển (Google Sheets)
#     DICTIONARY_URL = "https://docs.google.com/spreadsheets/d/1gcG0a6ZkXiJYxf7fgTCuzGNWTmcH6_XA/export?format=xlsx"

#     # Khởi tạo phân tích văn bản
#     analyzer = VietnameseTextAnalyzer(dictionary_url=DICTIONARY_URL)

#     # Kiểm tra từ điển
#     print("Một số từ trong từ điển:", list(analyzer.vietnamese_dict)[:20])

#     # Ví dụ sử dụng
#     test_sentence = "Hà Nội, năm 2025 sẽ là một năm tuyệt vời! Bạn nghĩ sao về điều này? Tôi đã đi 12.5km sáng nay."

#     # Phân tích câu
#     non_foreign_words, remaining_sentence = analyzer.analyze_sentence(test_sentence)

#     # In kết quả
#     print(f"Các từ không phải ngôn ngữ khác: {non_foreign_words}")
#     print(f"Câu còn lại (đã đánh dấu): {remaining_sentence}")
