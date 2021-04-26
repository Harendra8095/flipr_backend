from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()


def create_db_engine(config):
    engine = create_engine(config.DB_URL)
    return engine


def create_db_sessionFactory(engine):
    sessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
    return sessionFactory
