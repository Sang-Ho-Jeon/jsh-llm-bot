from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind == engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
    
# - autocommit -> 개발자가 db.commit() 데이터변경
# - autoflush -> db에 데이터를 보내는 것 // 작업을 효율적으로 관리할 수 있게 됩니다.