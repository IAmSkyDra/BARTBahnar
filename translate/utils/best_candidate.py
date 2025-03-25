from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class BestCandidateSelector:
    """
    Lớp này giúp lựa chọn từ ứng viên tốt nhất dựa trên ngữ cảnh
    bằng mô hình NlpHUST/gpt2-vietnamese.
    """

    def __init__(self, model_name="NlpHUST/gpt2-vietnamese", device=None):
        # Xác định thiết bị (CPU/GPU)
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")

        # Load mô hình và tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()  # Đặt model ở chế độ đánh giá

    def choose_best_candidate(self, context, candidates):
        """
        Chọn từ ứng viên phù hợp nhất dựa trên ngữ cảnh.
        
        Args:
            context (str): Câu ngữ cảnh trước từ cần chọn.
            candidates (list): Danh sách các ứng viên.

        Returns:
            str: Ứng viên tốt nhất hoặc "" nếu không có ứng viên hợp lệ.
        """
        if not candidates:  # Nếu danh sách rỗng, trả về ""
            return ""

        candidate_scores = {}

        for candidate in candidates:
            if not candidate:  # Bỏ qua ứng viên trống
                continue

            # Ghép ngữ cảnh với ứng viên
            input_text = f"{context} {candidate}"
            input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)

            # Tính xác suất cho từ ứng viên
            with torch.no_grad():
                outputs = self.model(input_ids)

            # Lấy logits cho token cuối cùng
            next_token_logits = outputs.logits[:, -1, :]

            # Tính điểm xác suất cho token cuối cùng
            score = next_token_logits[0, input_ids[0, -1]].item()

            # Lưu điểm xác suất của ứng viên
            candidate_scores[candidate] = score

        # Nếu không có ứng viên hợp lệ, trả về ""
        if not candidate_scores:
            return ""

        # Chọn ứng viên có điểm cao nhất
        return max(candidate_scores, key=candidate_scores.get)

# # Ví dụ sử dụng
# selector = BestCandidateSelector()
# context = "Ví dụ ngữ cảnh"
# candidates = ["ứng viên 1", "ứng viên 2", "ứng viên 3"]
# best_word = selector.choose_best_candidate(context, candidates)
# print("Best Candidate:", best_word)
