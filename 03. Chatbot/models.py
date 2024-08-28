from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI

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
# - (유저) 아 존나 느려 => 한국 서버를 안거치고 미국 웹서버(포워드 프록시 - 정적 파일)

def make_prompt(user_input):
  res = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
      {'role':'user', 'content': user_input},
      # {'role':'system', 'content':"안녕하세요. 환불 절차를 도와드리겠습니다. 고객님의 성함과 연락처를 입력해주세요."}
    ]
  )

  return res.choices[0].message.content

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == 'POST':
    
    user_input = request.form['user_input'] # 유저가 채팅창에 입력한 내용
    bot_response = make_prompt(user_input)

    messages.append({"role":"user", "text":user_input})
    messages.append({"role":"bot", "text":bot_response})

  return render_template('index.html', messages = messages)


if __name__ == "__main__":
  app.run(debug=True)