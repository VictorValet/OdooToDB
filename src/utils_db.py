import os

from dotenv import load_dotenv
from models import Base, User
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import Session
from typing import Type

load_dotenv()
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('PSQL_USER')}:{os.getenv('PSQL_PASSWORD')}@{os.getenv('PSQL_HOSTNAME')}:{os.getenv('PSQL_PROXY_PORT')}/{os.getenv('PSQL_DB')}",
    echo=True
)

def create_tables():
    Base.metadata.create_all(engine)

def create_or_update(model_class: Type[Base], record_data: dict):
    inspector = inspect(engine)
    if not inspector.has_table(model_class.__tablename__):
        create_tables()
    with Session(engine) as session:
        statement = select(model_class).where(model_class.id == record_data['id'])
        record = session.scalars(statement).first()
        if record:
            for key, value in record_data.items():
                setattr(record, key, value)
        else:
            record = model_class(**record_data)
            session.add(record)
        session.commit()

def get(model_class: Type[Base], id: int = None):
    try: 
        with Session(engine) as session:
            statement = select(model_class)
            if id:
                statement = statement.where(model_class.id == id)
            return session.scalars(statement).all()
    except Exception as e:
        return None

def delete(model_class: Type[Base], id: int):
    try:
        with Session(engine) as session:
            statement = select(model_class).where(model_class.id == id)
            record = session.scalars(statement).first()
            if record:
                session.delete(record)
                session.commit()
    except Exception as e:
        pass

def get_ids(model_class: Type[Base]):
    try:
        statement = select(model_class.id)
        with Session(engine) as session:
            return session.scalars(statement).all()
    except Exception as e:
        return None

def get_user_by_username(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.scalars(statement).first()
