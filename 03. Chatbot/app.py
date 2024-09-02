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

messages = [] # 메세지들이 담기는 공간 => 챗봇(채팅 내역 6개월동안 보관 법적으로 필요)

# 웹서버 - Nginx (리버스 프록시)
# (1) 로드 밸런서 => 트래픽 분산
# (2) 보안 => 다이렉트로 여러분들 자바 서버로 접근하게 되면 보안이 취약.

# (포워드 프록시)
# - 우리 회사가 미국에 런칭했어. 대박.
# - (유저) 아 느려 => 한국 서버를 안거치고 미국 웹서버(포워드 프록시 - 정적 파일)

def make_prompt(user_input):
  res = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=user_input
  )

  return res.choices[0].message.content # dict: 제공

@app.route('/', methods=["GET", "POST"])
def index():
    db = next(get_db())
    bot_response = ""
    if request.method == 'POST':
        user_input = request.form['user_input'] # 유저가 채팅창에 입력한 내용

        if user_input in ["안녕", "안녕하세요", "문의"]:
            conversation = [{"role":"system", "content":"You are a very kindful and helpful shopping mall C/S assistant"}]
            conversation.extend([{"role": msg['role'], "content":msg['content']} for msg in messages])
            conversation.append({"role":"user", "content":user_input})

            bot_response = make_prompt(conversation)

        else:
            name, email = extract_customer_name_email(user_input)
            print(name, email);
            query = text("SELECT * FROM users WHERE name= :name and email= :email")
            print(query)
            user = db.execute(query, {"name":name, "email":email}).fetchone()
            print(user)
            if user:
                bot_response = f"안녕하세요 고객님! 무엇을 도와드릴까요?"
                
                if '구매내역' in user_input :
                    query = text("SELECT * FROM purchases WHERE user_id= :user_id")
                    purchases = db.execute(query, {'user_id': user[0]}).fetchall()

                    if purchases:
                        purchase_detail = "\n".join(
                            [f"주문 내역: {p[0]}, {p[1], p[2]}" for p in purchases]
                        )
                        
                        bot_response = f"{user[2]}님의 주문 내역은 다음과 같습니다. {purchase_detail}"
                    else:
                        bot_response = '주문 내역이 확인되지 않습니다.'
                
                elif user_input in ['환불요청']:
                    query = text("SELECT * FROM purchases WHERE user_id= :user_id")
                    purchases = db.execute(query, {'user_id': user['id']}).fetchall()

                    if purchases:
                        purchase_detail = "\n".join(
                            [f"주문 내역: {p['id']}, {p['quality'], p['status']}" for p in purchases]
                        )
                        
                        bot_response = f"{user['name']}님의 주문 내역은 다음과 같습니다. {purchase_detail}"
                    else:
                        bot_response = '주문 내역이 확인되지 않습니다.'

        messages.append({'role':'user', 'content':user_input})
        messages.append({'role':'bot', 'content':bot_response})
        
    
    return render_template('index.html', messages=messages)

import re
def extract_customer_name_email(input_text):
  # 이름과 성함을 아래와 같이 입력해주세요.
  # 이름: 홍길동, 이메일: gildong@gmail.com

  # 정규표현식을 사용해서 이름과 이메일을 추출
  name_pattern = r"[가-힣][가-힣]*"
  email_pattern = r"[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}"

  name_match = re.search(name_pattern, input_text)
  email_match = re.search(email_pattern, input_text)

  name = name_match.group(0) if name_match else None
  email = email_match.group(0) if email_match else None

  return name, email

if __name__ == "__main__":
  app.run(debug=True)


# DB 연결 ->

# sqlite