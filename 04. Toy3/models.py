from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, CHAR, DECIMAL
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    
    isbn = Column(String(30), primary_key=True)
    cate_num = Column(String(30), nullable=False)
    title = Column(String(30), nullable=False)
    pub_name = Column(String(30), nullable=False)
    pub_date = Column(String(50), nullable=False)
    sale_stat = Column(String(30), nullable=False, default="판매중")
    sale_vol = Column(Integer, nullable=False, default=0)
    papr_pric = Column(Integer, nullable=False)
    e_pric = Column(Integer, nullable=False)
    papr_point = Column(DECIMAL(5, 2), nullable=False, default=5.0)
    e_point = Column(DECIMAL(5, 2), nullable=False, default=5.0)
    tot_page_num = Column(Integer, nullable=False)
    tot_book_num = Column(Integer, nullable=False)
    sale_com = Column(String(200), nullable=True)
    cont = Column(Text, nullable=True)
    rating = Column(DECIMAL(5, 2), nullable=True)
    info = Column(Text, nullable=True, comment='본문')
    intro_award = Column(Text, nullable=True)
    rec = Column(Text, nullable=True)
    pub_review = Column(Text, nullable=True)
    pre_start_page = Column(Integer, nullable=False)
    pre_end_page = Column(Integer, nullable=False)
    ebook_url = Column(String(100), nullable=False)
    book_reg_date = Column(DateTime, nullable=False, default=datetime.now)
    book_regi_id = Column(String(30), nullable=False, default='admin')
    reg_date = Column(DateTime, nullable=False, default=datetime.now)
    reg_id = Column(String(20), nullable=False, default='admin')
    up_date = Column(DateTime, nullable=False, default=datetime.now)
    up_id = Column(String(20), nullable=False, default='admin')
    
    # Relationships
    contributors = relationship('BookContributor', back_populates='book')
    images = relationship('BookImage', back_populates='book')
    discounts = relationship('BookDiscHist', back_populates='book')

class BookContributor(Base):
    __tablename__ = 'book_contributor'
    
    cb_num = Column(String(30), primary_key=True)
    isbn = Column(String(30), ForeignKey('book.isbn'), primary_key=True)
    reg_date = Column(DateTime, nullable=False, default=datetime.now)
    reg_id = Column(String(20), nullable=False, default='admin')
    up_date = Column(DateTime, nullable=False, default=datetime.now)
    up_id = Column(String(20), nullable=False, default='admin')
    
    # Relationships
    book = relationship('Book', back_populates='contributors')
    contributor = relationship('WritingContributor')

class BookImage(Base):
    __tablename__ = 'book_image'
    
    img_seq = Column(Integer, primary_key=True)
    isbn = Column(String(30), ForeignKey('book.isbn'), primary_key=True)
    img_url = Column(String(100), nullable=False)
    img_hrzt_size = Column(Integer, nullable=True)
    img_vrtc_size = Column(Integer, nullable=True)
    img_file_format = Column(String(30), nullable=True)
    img_regi_day = Column(DateTime, nullable=False, default=datetime.now)
    img_desc = Column(String(100), nullable=True)
    main_img_chk = Column(CHAR(1), nullable=True, default='N')
    reg_date = Column(DateTime, nullable=False, default=datetime.now)
    reg_id = Column(String(20), nullable=False, default='admin')
    up_date = Column(DateTime, nullable=False, default=datetime.now)
    up_id = Column(String(20), nullable=False, default='admin')
    
    # Relationships
    book = relationship('Book', back_populates='images')

class BookDiscHist(Base):
    __tablename__ = 'book_disc_hist'
    
    disc_seq = Column(Integer, primary_key=True)
    isbn = Column(String(30), ForeignKey('book.isbn'), primary_key=True)
    papr_disc = Column(DECIMAL(5, 2), nullable=False)
    e_disc = Column(DECIMAL(5, 2), nullable=False)
    disc_start_date = Column(DateTime, nullable=False)
    disc_end_date = Column(DateTime, nullable=False)
    comt = Column(String(100), nullable=True)
    reg_date = Column(DateTime, nullable=False, default=datetime.now)
    reg_id = Column(String(20), nullable=False, default='admin')
    up_date = Column(DateTime, nullable=False, default=datetime.now)
    up_id = Column(String(20), nullable=False, default='admin')
    
    # Relationships
    book = relationship('Book', back_populates='discounts')

class Category(Base):
    __tablename__ = 'category'
    
    cate_num = Column(String(30), primary_key=True)
    name = Column(String(30), nullable=False)
    lev = Column(Integer, nullable=False, default=1)
    last_cate_chk = Column(CHAR(1), nullable=False, default='N')
    cur_layr_num = Column(String(30), nullable=False, default='1')
    whol_layr_name = Column(String(255), nullable=True)
    reg_date = Column(DateTime, nullable=False, default=datetime.now)
    reg_id = Column(String(20), nullable=False, default='admin')
    up_date = Column(DateTime, nullable=False, default=datetime.now)
    up_id = Column(String(20), nullable=False, default='admin')

class WritingContributor(Base):
    __tablename__ = 'writing_contributor'
    
    cb_num = Column(String(30), primary_key=True)
    name = Column(String(30), nullable=False)
    job1 = Column(String(30), nullable=True)
    job2 = Column(String(30), nullable=True)
    cont_desc = Column(Text, nullable=True)
    wr_chk = Column(CHAR(1), nullable=True, default='N')
    reg_date = Column(DateTime, nullable=False, default=datetime.now)
    reg_id = Column(String(20), nullable=False, default='admin')
    up_date = Column(DateTime, nullable=False, default=datetime.now)
    up_id = Column(String(20), nullable=False, default='admin')
    
    # Relationships
    contributions = relationship('BookContributor', back_populates='contributor')