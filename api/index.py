# Nhập thêm thư viện CORS
from flask import Flask, jsonify
from flask_cors import CORS # <-- DÒNG MỚI
import feedparser

app = Flask(__name__)
CORS(app) # <-- DÒNG MỚI: Kích hoạt CORS cho toàn bộ ứng dụng

# URL của RSS feed từ Báo Đầu Tư
RSS_URL = "https://baodautu.vn/tai-chinh-chung-khoan.rss"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_news(path):
    try:
        feed = feedparser.parse(RSS_URL)
        news_items = []
        for entry in feed.entries:
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary,
                'published': entry.published
            })
        
        # Tạo một response và thêm header cho phép cache
        response = jsonify({
            'source': feed.feed.title,
            'articles': news_items
        })
        # Header này giúp Vercel cache lại kết quả trong 10 phút
        # giảm thời gian tải cho những lần gọi sau
        response.headers['Cache-Control'] = 's-maxage=600, stale-while-revalidate'
        
        return response # <-- THAY ĐỔI NHỎ: Trả về response đã tạo

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Không cần dòng if __name__ == '__main__' khi triển khai trên Vercel
