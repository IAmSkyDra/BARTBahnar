from collections import Counter, defaultdict
import math
import re
from config import CORPUS

class CorpusProcessor:
    """Xử lý dữ liệu văn bản: đọc corpus và tiền xử lý."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.corpus = self._load_corpus()

    def _load_corpus(self):
        """Đọc file văn bản và loại bỏ dòng trống."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]

    def get_corpus(self):
        """Trả về danh sách câu trong corpus."""
        return self.corpus


class PhraseExtractor:
    """Trích xuất các cụm từ có ý nghĩa từ corpus dựa trên chỉ số PMI."""

    def __init__(self, corpus, max_ngram=5, min_freq=2, min_pmi=3):
        self.corpus = corpus
        self.max_ngram = max_ngram
        self.min_freq = min_freq
        self.min_pmi = min_pmi
        self.phrase_dict = self._build_phrase_dict()

    def _build_phrase_dict(self):
        """Xây dựng từ điển cụm từ sử dụng chỉ số PMI."""

        ngram_counts = defaultdict(Counter)
        total_ngrams = defaultdict(int)
        word_counts = Counter()

        # 1) Duyệt từng câu trong corpus và đếm n-grams
        for sentence in self.corpus:
            words = re.findall(r'\w+', sentence)
            word_counts.update(words)

            for n in range(1, self.max_ngram + 1):
                if len(words) >= n:
                    ngrams = zip(*(words[i:] for i in range(n)))
                    ngram_list = list(ngrams)
                    ngram_counts[n].update(ngram_list)
                    total_ngrams[n] += len(ngram_list)

        phrase_dict = {}

        # 2) Tính PMI cho n-grams từ bậc 2 trở lên
        for n in range(2, self.max_ngram + 1):
            for ngram, count in ngram_counts[n].items():
                if count < self.min_freq:
                    continue

                p_ngram = count / total_ngrams[n]
                p_indep = math.prod(word_counts[w] / total_ngrams[1] for w in ngram)

                if p_indep <= 0:
                    continue

                pmi = math.log2(p_ngram / p_indep)
                if pmi >= self.min_pmi:
                    phrase_text = " ".join(ngram)
                    phrase_join = "_".join(ngram)
                    phrase_dict[phrase_text] = phrase_join

        return phrase_dict

    def get_phrases(self):
        """Trả về từ điển cụm từ."""
        return self.phrase_dict


class TextSegmenter:
    """Áp dụng từ điển cụm từ để phân đoạn văn bản."""

    def __init__(self):
        corpus_file = CORPUS
        corpus_processor = CorpusProcessor(corpus_file)
        corpus = corpus_processor.get_corpus()

        #Trích xuất cụm từ bằng PMI
        phrase_extractor = PhraseExtractor(corpus, max_ngram=3, min_freq=2, min_pmi=5)
        phrase_dict = phrase_extractor.get_phrases()
        self.phrase_dict = phrase_dict

    def segment(self, sentence):
        """Thay thế cụm từ bằng dạng gạch dưới."""

        sentence_lower = sentence.lower()
        for phrase, replacement in sorted(self.phrase_dict.items(), key=lambda x: -len(x[0])):
            pattern = rf"\b{re.escape(phrase)}\b"
            sentence_lower = re.sub(pattern, replacement, sentence_lower)

        return sentence_lower.split()


# # ===========================
# # **Sử dụng hệ thống OOP**
# # ===========================
# if __name__ == "__main__":
#     test_sentence = (
#         "'Bang nghiêm thu, 'bang thanh li hơp đông păng 'bang kuyêt toan đei yuêt dĭ kơpal đâu tư adrĭng khôi lươ̆ng tơgǔm pơm chơ đêh têh bal, keh kong tơdrong trong xe, thuy lơi nôi đông, tơdrong ǔnh rang tơgǔm choh jang nông nghiêp"
#     )

#     text_segmenter = TextSegmenter()
#     segmented_text = text_segmenter.segment(test_sentence)

#     print("\n=== Segmented Sentence ===")
#     print(segmented_text)
