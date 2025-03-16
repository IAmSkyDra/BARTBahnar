import json
import pandas as pd
from urllib3 import PoolManager
from urllib.parse import quote
from config import WORD_URL


class SolrClient:
    """
    Class để tương tác với Solr.
    """
    def __init__(self, solr_url):
        self.solr_url = solr_url.rstrip('/')
        self.http = PoolManager()

    def delete_all_documents(self):
        """
        Xóa toàn bộ dữ liệu trong Solr.
        """
        delete_query = '<delete><query>*:*</query></delete>'
        headers = {"Content-Type": "text/xml"}
        response = self.http.request('POST', f'{self.solr_url}/update?commit=true', body=delete_query, headers=headers)

        if response.status == 200:
            print("All data on Solr has been deleted.")
        else:
            print(f"❌ Lỗi khi xóa dữ liệu: {response.status}, {response.data.decode('utf-8')}")

    def upload_documents(self, data):
        """
        Tải dữ liệu lên Solr.
        """
        headers = {'Content-Type': 'application/json'}
        response = self.http.request('POST', f'{self.solr_url}/update?commit=true', body=json.dumps(data).encode('utf-8'), headers=headers)

        if response.status == 200:
            print("The data has been successfully uploaded to Solr!")
        else:
            print(f"❌ Lỗi khi tải dữ liệu lên Solr: {response.data.decode('utf-8')}")

    def search_bahnar_words(self, words):
        """
        Tìm kiếm danh sách từ Bahnar trong Solr và trả về danh sách các cặp từ Bahnar - tiếng Việt.
        """
        or_query = " OR ".join([f'bahnar:"{quote(word)}"' for word in words])
        search_url = f'{self.solr_url}/select?indent=true&q.op=OR&q=({or_query})&rows=1000&fl=bahnar,vietnamese&wt=json'

        response = self.http.request('GET', search_url)

        try:
            data = json.loads(response.data.decode('utf-8'))
        except json.JSONDecodeError:
            # print("❌ Không thể giải mã phản hồi từ Solr.")
            return []

        if 'response' not in data:
            # print(f"❌ Lỗi từ Solr: {data.get('error', 'Không có thông tin lỗi')}")
            return []

        results = {}
        for doc in data['response']['docs']:
            bahnar_word = doc.get('bahnar', [''])[0]
            vietnamese_word = doc.get('vietnamese', [''])[0]

            if bahnar_word and vietnamese_word:
                if bahnar_word not in results:
                    results[bahnar_word] = []
                results[bahnar_word].append(vietnamese_word)

        final_results = [{"bahnar": k, "vietnamese": list(set(v))} for k, v in results.items()]
        return final_results


class GoogleSheetsClient:
    """
    Class để xử lý dữ liệu từ Google Sheets.
    """
    def __init__(self, sheet_url):
        self.sheet_url = sheet_url

    def read_csv(self):
        """
        Đọc dữ liệu từ Google Sheets dưới dạng CSV.
        """
        df = pd.read_csv(self.sheet_url)
        return df[['tiếng bana', 'tiếng việt']].rename(columns={'tiếng bana': 'tieng_bana', 'tiếng việt': 'tieng_viet'})


class SearchTranslator:
    """
    Class để tìm kiếm và dịch từ Bahnar sang tiếng Việt.
    """
    def __init__(self, solr_url):
        # Khởi tạo các đối tượng
        solr_client = SolrClient(solr_url)
        google_sheets_client = GoogleSheetsClient(WORD_URL)

        # Đọc dữ liệu từ Google Sheets
        df = google_sheets_client.read_csv()

        # Xóa dữ liệu cũ trên Solr
        solr_client.delete_all_documents()

        # Chuẩn bị dữ liệu để tải lên Solr
        documents = [{"bahnar": row["tieng_bana"], "vietnamese": row["tieng_viet"]} for _, row in df.iterrows()]

        # Tải dữ liệu lên Solr
        solr_client.upload_documents(documents)
        self.solr_client = solr_client
        self.solr_url = solr_url

    def deleteQuery(self, url = 'http://localhost:8983/solr/mycore/update?commit=true'):
        http = PoolManager()
        r = http.request('POST', url, body=b'<delete><query>*:*</query></delete>', headers={'Content-Type': 'text/xml'})
        return

    def search(self, words):
        """
        Tìm kiếm danh sách từ Bahnar trong Solr.
        """
        self.deleteQuery(self.solr_url)
        return self.solr_client.search_bahnar_words(words)


# # ===================== Cấu hình ===================== #
# solr_url = 'https://0308-2001-ee0-d748-add0-55f5-2481-1d52-57aa.ngrok-free.app/solr/mycore'
# sheet_url = WORD_URL

# # Khởi tạo các đối tượng
# translator = SearchTranslator(solr_url)

# # ===================== Tìm kiếm từ Bahnar ===================== #
# words_to_search = ['tơdrong', 'pơm', 'hanh_vi', '<word>', 'ruốt', 'tĕch', 'hoa_chât', '<word>', 'khang_sinh', 'bĭ', 'ăn', 'jung', 'lơm', 'rong_pơtăm_thuy_san', '<word>']
# search_results = translator.search(words_to_search)

# print("🔎 Kết quả tìm kiếm:")
# print(json.dumps(search_results, indent=4, ensure_ascii=False))
