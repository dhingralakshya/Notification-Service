# define database model and intialize db
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./notifications.db" #create a file name notifications.db in current directory
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# notification model(table)
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)  
    user_id = Column(String, index=True)
    notif_type = Column(String)
    content = Column(Text)
    status = Column(String, default="pending") # pending || sent || failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# create tables if they don't exist
def init_db():
    Base.metadata.create_all(bind=engine)
