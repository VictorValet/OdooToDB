import os
from typing import Type

from dotenv import load_dotenv
from models import Base, User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

load_dotenv()
engine = create_engine(
	f"postgresql+psycopg2://{os.getenv('PSQL_USER')}:{os.getenv('PSQL_PASSWORD')}@{os.getenv('PSQL_HOSTNAME')}:{os.getenv('PSQL_PROXY_PORT')}/{os.getenv('PSQL_DB')}",
	echo=True
)

def create_tables():
    Base.metadata.create_all(engine)

def create_or_update(model_class: Type[Base], record_data: dict):
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
    with Session(engine) as session:
        statement = select(model_class)
        if id:
            statement = statement.where(model_class.id == id)
        return session.scalars(statement).all()

def delete(model_class: Type[Base], id: int):
    with Session(engine) as session:
        statement = select(model_class).where(model_class.id == id)
        record = session.scalars(statement).first()
        if record:
            session.delete(record)
            session.commit()

def get_ids(model_class: Type[Base]):
    statement = select(model_class.id)
    with Session(engine) as session:
        return session.scalars(statement).all()

def get_user_by_username(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.scalars(statement).first()
