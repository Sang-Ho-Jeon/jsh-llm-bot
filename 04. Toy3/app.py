from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS 모듈 추가
from dotenv import load_dotenv
import os
from openai import OpenAI
from database import get_db
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)
CORS(app)  # CORS 설정 적용

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

messages = []  # 메세지들이 담기는 공간

def make_prompt(user_input):
    res = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=user_input
    )

    return res.choices[0].message.content  # dict: 제공

@app.route('/', methods=["POST"])
def index():
    db = next(get_db())
    bot_response = ""
    books_data = []
    faqs_data = []

    data = request.json
    user_input = data.get('user_input')
    search_type = data.get('search_type')
    print(f"User Input: {user_input}, Search Type: {search_type}")

    if search_type == 'book':
        query = text("""
            SELECT isbn, pub_name, pub_date, sale_stat, sale_vol, papr_pric, e_pric, sale_com, pub_review, title 
            FROM book 
            WHERE title LIKE :title
        """)
        books = db.execute(query, {"title": f"%{user_input}%"}).fetchall()
        print(books)
        
        if books:
            books_data = [
                {
                    "title": book.title,
                    "isbn": book.isbn,
                    "pub_name": book.pub_name,
                    "pub_date": book.pub_date,
                    "sale_stat": book.sale_stat,
                    "sale_vol": book.sale_vol,
                    "papr_pric": book.papr_pric,
                    "e_pric": book.e_pric,
                    "sale_com": book.sale_com,
                    "pub_review": book.pub_review,
                }
                for book in books
            ]
            bot_response = "다음은 검색된 책들입니다."
        else:
            bot_response = "해당 책을 찾을 수 없습니다."

    elif search_type == 'faq':
        query = text("""
            SELECT title, cont, view_cnt 
            FROM faq 
            WHERE title LIKE :input OR cont LIKE :input
        """)
        faqs = db.execute(query, {"input": f"%{user_input}%"}).fetchall()
        print(faqs)

        if faqs:
            faqs_data = [
                {
                    "title": faq.title,
                    "cont": faq.cont,
                    "view_cnt": faq.view_cnt,
                }
                for faq in faqs
            ]
            bot_response = "다음은 검색된 FAQ 항목들입니다."
        else:
            bot_response = "해당 FAQ 항목을 찾을 수 없습니다."

    return jsonify({
        'bot_response': bot_response,
        'books': books_data,
        'faqs': faqs_data
    })

if __name__ == "__main__":
    app.run(debug=True)