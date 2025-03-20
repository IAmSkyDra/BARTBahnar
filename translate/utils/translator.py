class Translate_Model:
    def __init__(self, model_name="IAmSkyDra/BARTBana_Translation"):
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

        # Tải mô hình và tokenizer một lần khi khởi tạo
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def translate(self, word):
        # Dịch từ
        inputs = self.tokenizer(word, return_tensors="pt", truncation=True)
        outputs = self.model.generate(inputs["input_ids"])
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translation

# Ví dụ sử dụng
# word = "ngiêm"
# translated_word = translator.translate(word)
# print(f"Translated word: {translated_word}")
