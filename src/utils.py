from contextlib import contextmanager
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def get_psql_conn():
    return psycopg2.connect(
        database=os.getenv('PSQL_DB'),
        host=os.getenv('PSQL_HOSTNAME'),
        user=os.getenv('PSQL_USER'),
        password=os.getenv('PSQL_PASSWORD'),
        port=os.getenv('PSQL_PROXY_PORT')
    )

@contextmanager
def psql_conn():
    conn = get_psql_conn()
    try:
        yield conn
    finally:
        conn.close()
