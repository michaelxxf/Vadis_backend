from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# MySQL connection URL (adjust your DB name, user, and password)
DATABASE_URL = "mysql+pymysql://root:@localhost/vadis"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# ✅ This is the function you're trying to import
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()