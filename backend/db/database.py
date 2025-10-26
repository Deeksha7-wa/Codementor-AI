from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

DATABASE_URL = "sqlite:///./submissions.db"  # synchronous SQLite

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="anonymous")
    language = Column(String)
    code = Column(Text)
    errors = Column(Text)        # store JSON as string
    hints = Column(Text)         # store JSON as string
    suggestions = Column(Text)   # store JSON as string
    timestamp = Column(String, default=str(datetime.datetime.utcnow()))

# ✅ Synchronous init_db function
def init_db():
    Base.metadata.create_all(bind=engine)
