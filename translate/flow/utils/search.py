from urllib3 import *
from urllib.parse import quote as qoute
import json
import csv
import pandas as pd
import xlsxwriter as xlsx
from tqdm import tqdm  # Add tqdm for progress bar
import gspread
import pandas as pd
import json
from urllib3 import PoolManager
import request

## Delete query
def deleteQuery(url = 'http://localhost:8983/solr/mycore/update?commit=true'):
    http = PoolManager()
    r = http.request('POST', url, body=b'<delete><query>*:*</query></delete>', headers={'Content-Type': 'text/xml'})
    return


# Đọc dữ liệu từ Google Sheets dưới dạng CSV (không cần xác thực)
def read_google_sheet_csv(sheet_url):
    # Đọc CSV từ Google Sheets trực tiếp
    df = pd.read_csv(sheet_url)
    return df

# Hàm tải dữ liệu lên Solr
def upload_to_solr(df, solr_url='http://localhost:8983/solr/my_core/update?commit=true'):

    # Xóa toàn bộ dữ liệu
    delete_query = '<delete><query>*:*</query></delete>'
    headers = {"Content-Type": "text/xml"}
    response = requests.post(solr_url, data=delete_query, headers=headers)

    # Kiểm tra phản hồi
    if response.status_code == 200:
        print("Đã xóa toàn bộ dữ liệu trên Solr.")
    else:
        print(f"Lỗi khi xóa dữ liệu: {response.status_code}, {response.text}")

    http = PoolManager()  # Tạo PoolManager
    headers = {'Content-Type': 'application/json'}

    # Chuẩn bị dữ liệu để gửi lên Solr (chỉ lấy cột tiếng Bahnar và tiếng Việt)
    data = []
    for index, row in df.iterrows():
        document = {
            "bahnar": row['tieng_bana'],  # Từ Bahnar
            "vietnamese": row['tieng_viet']  # Từ tiếng Việt
        }
        data.append(document)

    # Gửi yêu cầu POST lên Solr
    response = http.request('POST', solr_url, body=json.dumps(data).encode('utf-8'), headers=headers)

    if response.status == 200:
        print("Dữ liệu đã được tải lên Solr thành công!")
    else:
        print(f"Lỗi khi tải dữ liệu lên Solr: {response.data.decode('utf-8')}")

# # Ví dụ sử dụng:
# sheet_url = "https://docs.google.com/spreadsheets/d/your_spreadsheet_id_here/edit#gid=0"  # Đường link của Google Sheets
# df = read_google_sheet(sheet_url)

# # Chỉ lấy 2 cột 'tiếng bana' và 'tiếng việt' từ Google Sheets
# df = df[['tiếng bana', 'tiếng việt']]

# # Tải lên Solr
# upload_to_solr(df)

# # Ví dụ sử dụng:
sheet_url = "https://docs.google.com/spreadsheets/d/1xVXW1d784zC12b24dQoQJtWZyfgwrX-l/export?format=csv&id=1xVXW1d784zC12b24dQoQJtWZyfgwrX-l"  # Đường link của Google Sheets
df = read_google_sheet_csv(sheet_url)

# Chỉ lấy 2 cột 'tiếng bana' và 'tiếng việt' từ Google Sheets
df = df[['tiếng bana', 'tiếng việt']]
# Đổi tên cột thành tên không có dấu và không có khoảng trắng
df = df.rename(columns={
    'tiếng bana': 'tieng_bana',
    'tiếng việt': 'tieng_viet'
})

# Cấu hình
solr_url = 'https://0308-2001-ee0-d748-add0-55f5-2481-1d52-57aa.ngrok-free.app/solr/mycore'
# Tải lên Solr
upload_to_solr(df, f'{solr_url}/update?commit=true')


from urllib.parse import quote
from urllib3 import PoolManager
import json

def batchFindVietnamese(words, url='https://a312-2001-ee0-d748-8aa0-6dc1-5d4b-3762-1be3.ngrok-free.app/solr/mycore/select?indent=true&q.op=OR&q='):
    """
    Tìm kiếm nhiều từ Bahnar cùng một lúc và trả về kết quả với tiếng Bahnar và tiếng Việt dưới dạng list.
    """
    http = PoolManager()

    # Tạo truy vấn ghép tất cả từ với "OR" và bao quanh mỗi từ bằng dấu ngoặc kép để tìm chính xác từ
    or_query = " OR ".join([f"bahnar:\"{quote(word)}\"" for word in words])  # Sử dụng dấu ngoặc kép để tìm chính xác
    solr_url = f"{url}({or_query})&rows=1000&fl=bahnar,vietnamese&wt=json"

    # Thực hiện truy vấn
    response = http.request('GET', solr_url)

    try:
        data = json.loads(response.data.decode('utf-8'))
    except json.JSONDecodeError:
        print("Không thể giải mã phản hồi từ Solr.")
        return []

    # Kiểm tra nếu phản hồi không chứa 'response'
    if 'response' not in data:
        print(f"Lỗi từ Solr: {data.get('error', 'Không có thông tin lỗi')}")
        return []

    # Xử lý kết quả và nhóm các từ tiếng Việt cho mỗi từ tiếng Bahnar
    results = {}
    for doc in data['response']['docs']:
        bahnar_word = doc.get('bahnar', '')  # Lấy từ tiếng Bahnar
        vietnamese_word = doc.get('vietnamese', '')  # Lấy từ tiếng Việt

        if bahnar_word and vietnamese_word:
            bahnar_word = bahnar_word[0]  # Đảm bảo lấy từ đầu tiên nếu nhiều giá trị
            if bahnar_word not in results:
                results[bahnar_word] = []  # Khởi tạo danh sách cho từ Bahnar nếu chưa có
            results[bahnar_word].append(vietnamese_word[0])  # Thêm từ Việt vào danh sách

    # Chuyển đổi kết quả thành dạng list các từ tiếng Việt cho mỗi từ tiếng Bahnar
    final_results = [{"bahnar": bahnar, "vietnamese": list(set(vietnamese))} for bahnar, vietnamese in results.items()]

    return final_results

# Ví dụ sử dụng
words = ['tơdrong', 'pơm', 'hanh_vi', '<word>', 'ruốt', 'tĕch', 'hoa_chât', '<word>', 'khang_sinh', 'bĭ', 'ăn', 'jung', 'lơm', 'rong_pơtăm_thuy_san', '<word>']  # Danh sách từ cần tìm kiếm
results = batchFindVietnamese(words)
print(results)

def search(words, solr_url):
    """
    Tìm kiếm từ Bahnar trong Solr và trả về kết quả.
    # Xóa dữ liệu cũ trong Solr trước khi tải dữ liệu mới
    # Tìm kiếm các từ từ file input (ví dụ: file Excel)
    """
    deleteQuery(solr_url)
    # print('OKe')
    return batchFindVietnamese(words, solr_url)