import spacy
import re
import requests
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Tải tokenizer và mô hình từ UnderTheSea
tokenizer = AutoTokenizer.from_pretrained("undertheseanlp/vietnamese-ner-v1.4.0a2")
model = AutoModelForTokenClassification.from_pretrained("undertheseanlp/vietnamese-ner-v1.4.0a2")

# Khởi tạo pipeline NER
ner_model = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Khởi tạo spaCy model
nlp_spacy = spacy.blank("vi")

# Tải từ điển tiếng Việt từ file .xlsx với pandas
def load_vietnamese_dictionary(file_path="vietnamese_words.xlsx"):
    df = pd.read_excel(file_path, usecols=[0], header=None)
    vietnamese_words = set(df[0].str.strip().str.lower().dropna())
    return vietnamese_words

# Tải từ điển từ Google Sheets (exported as XLSX)
def download_vietnamese_dictionary(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Từ điển đã được tải và lưu tại: {file_path}")
    else:
        print(f"Không thể tải từ điển. Mã lỗi: {response.status_code}")

def is_special_character(word):
    # Kiểm tra nếu từ chứa bất kỳ ký tự nào trong chuỗi punctuation
    punctuations = "#$%&()*+,-./:;<=>?@[\]^`{}~"
    return bool(re.match(f"[{re.escape(punctuations)}]", word))

# Kiểm tra từ viết hoa
def is_capitalized(word):
    return word[0].isupper()

# Kiểm tra từ có phải tiếng Việt
def is_vietnamese_word(word, vietnamese_dict):
    return word.lower() in vietnamese_dict

# Kiểm tra từ có phải số
def is_number(word):
    return word.isdigit() or bool(re.match(r"^0*\d+(\.\d+)?$", word))

# Kiểm tra từ có phải ngày tháng năm dạng số
def is_date(word):
    # Kiểm tra các định dạng ngày tháng năm phổ biến
    date_formats = [
        r"^\d{1,2}/\d{1,2}/\d{4}$",  # dd/mm/yyyy
        r"^\d{1,2}-\d{1,2}-\d{4}$",  # dd-mm-yyyy
        r"^\d{4}/\d{1,2}/\d{1,2}$",  # yyyy/mm/dd
        r"^\d{4}-\d{1,2}-\d{1,2}$",  # yyyy-mm-dd
    ]
    return any(re.match(date_format, word) for date_format in date_formats)

# Phân tích câu trực tiếp từ mô hình
def analyze_sentence_with_model(sentence, vietnamese_dict):
    # Sử dụng spaCy tokenizer để token hóa câu
    doc = nlp_spacy(sentence)
    tokens = [token.text for token in doc]

    results = []

    # Phân loại từng từ được nhận diện
    for word in tokens:
        # Kiểm tra ký tự đặc biệt
        if is_special_character(word):
            results.append((word, "Ký tự đặc biệt"))
        # Kiểm tra số
        elif is_number(word):
            results.append((word, "Số"))
        # Kiểm tra ngày tháng năm dạng số
        elif is_date(word):
            results.append((word, "Ngày tháng năm"))
        # Kiểm tra từ tiếng Việt
        elif is_vietnamese_word(word, vietnamese_dict):
            results.append((word, "Tiếng Việt"))
        # Ngôn ngữ khác
        else:
            results.append((word, "Ngôn ngữ khác"))

    # # Chạy mô hình NER để nhận diện các thực thể
    # ner_results = ner_model(sentence)
    # for entity in ner_results:
    #     results.append((entity['word'], entity['entity_group']))
    # print(results)
    # Giữ lại các từ không phải ngôn ngữ khác
    non_foreign_words = [word for word, category in results if category != "Ngôn ngữ khác"]

    # Tạo câu còn lại với các phần không phải ngôn ngữ khác và đánh dấu
    remaining_sentence = " ".join([f"<word>" if category != "Ngôn ngữ khác" else word
                                   for word, category in results])

    return non_foreign_words, remaining_sentence

def normalize_words(word_list):
    normalized_list = []
    for word in word_list:
        # Loại bỏ dấu gạch dưới và chuyển thành chữ thường
        normalized_word = word.replace('_', ' ').lower()
        normalized_list.append(normalized_word)
    return normalized_list

# Tải từ điển từ Google Sheets (exported as XLSX)
DICTIONARY_URL = "https://docs.google.com/spreadsheets/d/1gcG0a6ZkXiJYxf7fgTCuzGNWTmcH6_XA/export?format=xlsx"
DICTIONARY_FILE = "vietnamese_words.xlsx"
download_vietnamese_dictionary(DICTIONARY_URL, DICTIONARY_FILE)
vietnamese_dict = load_vietnamese_dictionary(DICTIONARY_FILE)

# In ra một số từ trong từ điển để kiểm tra
print("Một số từ trong từ điển:", list(vietnamese_dict)[:20])

# Ví dụ sử dụng
sentence = "Hôm nay là ngày 12/05/2023, nhiệt độ là 25.5 độ C."
non_foreign_words, remaining_sentence = analyze_sentence_with_model(sentence, vietnamese_dict)
print("Các từ không phải ngôn ngữ khác:", non_foreign_words)
print("Câu còn lại:", remaining_sentence)

# Câu ví dụ
test_sentence = "Hà Nội, năm 2025 sẽ là một năm tuyệt vời! Bạn nghĩ sao về điều này? Tôi đã đi 12.5km sáng nay."

# Phân tích câu
non_foreign_words, remaining_sentence = analyze_sentence_with_model(test_sentence, vietnamese_dict)

# In kết quả
print(f"Các từ không phải ngôn ngữ khác: {non_foreign_words}")
print(f"Câu còn lại (đã đánh dấu): {remaining_sentence}")

