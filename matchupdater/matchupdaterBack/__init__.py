from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_db_engine(config):
    engine = create_engine(config.DB_URL)
    return engine


def create_db_sessionFactory(engine):
    sessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
    return sessionFactory
