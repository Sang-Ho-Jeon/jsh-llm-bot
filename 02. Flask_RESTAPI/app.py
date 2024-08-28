from flask import Flask, request
from routes import register_routes


app = Flask(__name__)
register_routes(app)

@app.route('/')
def index():
    return {"Hello":"Flask!"}

# 간단한 API 만들어보겠습니다.
@app.route('/api/v1/feeds', methods=['GET']) # REST API: [GET] /api/v1/feeds
def show_all_feeds():
    data = {'result':'success', 'data':{'feed1':'data1', 'feed2':'data2'}}
    # 데이터 타입: 파이썬 Dict => 브라우저가 이해할 수 없어요.

    return data # jsonify

@app.route('/api/v1/feeds/<int:feed_id>', methods=['GET'])
def show_one_feed(feed_id):
    data = {'result':'success', 'data':f'feed ID: {feed_id}'}
    return data

# java: request(요청) => flask python
@app.route('/api/v1/feeds', methods=['POST'])
def create_feed():
    email = request.form['email']
    content = request.form['content']
    data = {'result':'success', 'data': {'email':email, 'contet':content}}

    return data


if __name__ == "__main__":
    app.run(debug=True)
    
    # 마이크로서비스 아키텍처 -> 왜 이렇게 할까요? -> 하나 터져도 다른 기능은 문제X.
    # 배달의 민족
    # - 결제기능 => 기능 하나당 서버 하나.
    # - 주문기능
    # - 라이더배송기능
    # - .....
    
    # 메인 디비는 하나.