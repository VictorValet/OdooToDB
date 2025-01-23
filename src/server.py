import utils
from fastapi import FastAPI, HTTPException
from psycopg2 import OperationalError, ProgrammingError

def fetch(fetch_request: str, fetch_method, message_404: str):
    try:
        with utils.psql_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(fetch_request)
                data = fetch_method(cursor)
        if not data:
            raise HTTPException(status_code=404, detail=message_404)
        return data
    except (OperationalError, ProgrammingError) as e:
        raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()

@app.get("/contacts")
def fetch_contacts():
    return fetch(
        (f"SELECT * FROM contacts"),
        lambda cursor: cursor.fetchall(),
        "No contact found"
    )

@app.get("/contacts/{contact_id}")
def fetch_contact(contact_id: int):
    return fetch(
        (f"SELECT * FROM contacts WHERE id = {contact_id}"),
        lambda cursor: cursor.fetchone(),
        "Contact not found"
    )

@app.get("/invoices")
def fetch_invoices():
    return fetch(
        (f"SELECT * FROM invoices"),
        lambda cursor: cursor.fetchall(),
        "No invoice found"
    )

@app.get("/invoices/{invoice_id}")
def fetch_invoice(invoice_id: int):
    return fetch(
        (f"SELECT * FROM invoices WHERE id = {invoice_id}"),
        lambda cursor: cursor.fetchone(),
        "Invoice not found"
    )
