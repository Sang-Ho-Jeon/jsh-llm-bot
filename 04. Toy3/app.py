from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI
from database import get_db
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

messages = []  # 메세지들이 담기는 공간

def make_prompt(user_input):
    res = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=user_input
    )

    return res.choices[0].message.content  # dict: 제공

@app.route('/', methods=["GET", "POST"])
def index():
    db = next(get_db())
    bot_response = ""
    if request.method == 'POST':
        user_input = request.form['user_input']  # 유저가 채팅창에 입력한 내용
        print(user_input)
        
        # 책 제목이 포함된 모든 책들을 가져오기
        query = text("""
            SELECT isbn, pub_name, pub_date, sale_stat, sale_vol, papr_pric, e_pric, sale_com, pub_review 
            FROM book 
            WHERE title LIKE :title
        """)
        books = db.execute(query, {"title": f"%{user_input}%"}).fetchall()
        print(books)
        
        if books:
            book_details = [
                (
                    f"책 제목: {user_input}\n"
                    f"ISBN: {book.isbn}\n"
                    f"출판사: {book.pub_name}\n"
                    f"출판일: {book.pub_date}\n"
                    f"판매 상태: {book.sale_stat}\n"
                    f"판매량: {book.sale_vol}\n"
                    f"종이책 가격: {book.papr_pric}원\n"
                    f"전자책 가격: {book.e_pric}원\n"
                    f"판매 회사: {book.sale_com}\n"
                    f"출판사 리뷰: {book.pub_review}\n"
                )
                for book in books
            ]
            bot_response = "\n\n".join(book_details)
        else:
            bot_response = "해당 책을 찾을 수 없습니다."

        messages.append({'role': 'user', 'content': user_input})
        messages.append({'role': 'bot', 'content': bot_response})

    return render_template('index.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)