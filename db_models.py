from sqlalchemy import create_engine, Column, Integer, String, BigInteger, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import declarative_base, sessionmaker
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}/{getenv('DB_SCHEME')}"
engine = create_engine(DATABASE_URL, pool_recycle=299, pool_pre_ping=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    tg_id = Column(BigInteger, unique=True, nullable=False)
    degreas_percent = Column(Integer)
    increas_percent = Column(Integer)
    signal_interval = Column(JSON)
    signals_history = Column(LONGTEXT)
    email = Column(String(255))
    lang = Column(String(10))
