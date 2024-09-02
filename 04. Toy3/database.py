from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# MySQL 데이터베이스 설정
DATABASE_URL = 'mysql+pymysql://springPracUser:1234@localhost/book_shop'

# MySQL 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 생성기 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # 모델에서 정의된 테이블 생성
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 초기화
init_db()