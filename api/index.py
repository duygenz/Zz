from flask import Flask, jsonify
import feedparser

app = Flask(__name__)

# URL của RSS feed từ Báo Đầu Tư
RSS_URL = "https://baodautu.vn/tai-chinh-chung-khoan.rss"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_news(path):
    try:
        # Phân tích cú pháp RSS feed từ URL
        feed = feedparser.parse(RSS_URL)

        # Trích xuất thông tin cần thiết từ mỗi bài viết
        news_items = []
        for entry in feed.entries:
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary,
                'published': entry.published
            })

        # Trả về dữ liệu dưới dạng JSON
        return jsonify({
            'source': feed.feed.title,
            'articles': news_items
        })

    except Exception as e:
        # Xử lý nếu có lỗi xảy ra
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
