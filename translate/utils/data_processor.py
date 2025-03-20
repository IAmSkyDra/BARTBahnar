import pandas as pd
import os

class DataProcessor:
    def __init__(self, output_dir="../data"):
        """
        Khởi tạo với danh sách URL cố định và thư mục đầu ra.
        """
        self.urls = [
            "https://docs.google.com/spreadsheets/d/1_lcoKY79oM7WsDCM1-yCQ24kZzL99NU-/export?format=csv",
            "https://docs.google.com/spreadsheets/d/1lvpUQC4VWqYFHGmsqbeC-pVeTnmltdah/export?format=csv",
            "https://docs.google.com/spreadsheets/d/1jnX96jO81FZVRJQ6iy-b_7SMtFztOtIt/export?format=csv"
        ]
        self.output_dir = output_dir
        self.dataframes = []
        self.rows_per_file = []
        self.rows_removed = 0
        self.removed_rows_info = []
        self.duplicates_removed = 0
        self.merged_df = None

        # Tạo thư mục nếu chưa có
        os.makedirs(self.output_dir, exist_ok=True)

    def load_and_clean_data(self):
        """
        Đọc dữ liệu từ các URL, loại bỏ hàng không hợp lệ và dữ liệu trùng lặp.
        """
        for url in self.urls:
            df = pd.read_csv(url)

            if "tiếng bana" in df.columns and "tiếng việt" in df.columns:
                initial_rows = df.shape[0]
                self.rows_per_file.append(initial_rows)

                # Tìm các hàng có một cột bị thiếu
                invalid_rows = df[(df["tiếng bana"].isna() & ~df["tiếng việt"].isna()) |
                                  (~df["tiếng bana"].isna() & df["tiếng việt"].isna())]

                self.rows_removed += invalid_rows.shape[0]
                self.removed_rows_info.append((url, invalid_rows.index.tolist()))

                # Loại bỏ hàng không hợp lệ
                df = df.drop(invalid_rows.index)
                self.dataframes.append(df[["tiếng bana", "tiếng việt"]])

        # Gộp tất cả các DataFrame lại
        self.merged_df = pd.concat(self.dataframes, ignore_index=True)

        # Xóa các bản ghi trùng lặp
        initial_merged_rows = self.merged_df.shape[0]
        self.merged_df = self.merged_df.drop_duplicates(subset=["tiếng bana"]).drop_duplicates(subset=["tiếng việt"])
        self.duplicates_removed = initial_merged_rows - self.merged_df.shape[0]

    def save_clean_data(self, output_filename="final.csv"):
        """
        Lưu dữ liệu đã xử lý vào file CSV trong thư mục 'data/'.
        """
        output_path = os.path.join(self.output_dir, output_filename)
        if self.merged_df is not None:
            self.merged_df.to_csv(output_path, index=False)
            # print(f"✅ Dữ liệu sạch đã được lưu vào {output_path}")
        else:
            print("⚠️ Không có dữ liệu để lưu!")

    def extract_sentences(self, column_name="tiếng bana", output_filename="bana_data.txt"):
        """
        Trích xuất câu từ một cột cụ thể và lưu vào file văn bản trong thư mục 'data/'.
        """
        if self.merged_df is None or column_name not in self.merged_df.columns:
            raise ValueError(f"⚠️ Cột '{column_name}' không tồn tại hoặc dữ liệu chưa được load!")

        # Chuẩn hóa và loại bỏ khoảng trắng
        self.merged_df[column_name] = self.merged_df[column_name].str.normalize('NFKC').str.strip()

        # Lọc các câu duy nhất
        sentences = self.merged_df[column_name].dropna().str.strip().unique()

        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            for sentence in sentences:
                if sentence:
                    f.write(sentence + "\n")

        # print(f"✅ Đã lưu {len(sentences)} câu vào '{output_path}'")

    def print_summary(self):
        """
        In tóm tắt quá trình xử lý dữ liệu.
        """
        # print("📊 Tóm tắt quá trình xử lý dữ liệu:")
        # print("Tổng số file:", len(self.urls))
        # print("Số hàng trong từng file ban đầu:", self.rows_per_file)
        # print("Số hàng bị xóa do chỉ có giá trị ở một cột:", self.rows_removed)
        # print("Số hàng trùng lặp bị xóa:", self.duplicates_removed)
        # print("Số hàng còn lại sau khi xử lý:", self.merged_df.shape[0] if self.merged_df is not None else 0)
        # print("Địa chỉ của các hàng bị xóa:")
        # for file, rows in self.removed_rows_info:
        #     print(f"File: {file}, Hàng bị xóa: {rows}")
