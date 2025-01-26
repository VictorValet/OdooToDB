import bcrypt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from psycopg2 import OperationalError, ProgrammingError
import utils
import utils_jwt

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form : OAuth2PasswordRequestForm = Depends()):
    credentials = fetch(
        (f"SELECT * FROM users WHERE username = '{form.username}'"),
        lambda cursor: cursor.fetchone(),
        "User not found"
    )
    if bcrypt.checkpw(form.password.encode("utf-8"), credentials[2].encode("utf-8")):
        access_token = utils_jwt.create_access_token(data={"sub": form.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/contacts")
def fetch_contacts(token: str = Depends(oauth2_scheme)):
    utils_jwt.verify_token(token)
    return fetch(
        (f"SELECT * FROM contacts"),
        lambda cursor: cursor.fetchall(),
        "No contact found"
    )

@app.get("/contacts/{contact_id}")
def fetch_contact(contact_id: int, token: str = Depends(oauth2_scheme)):
    utils_jwt.verify_token(token)
    return fetch(
        (f"SELECT * FROM contacts WHERE id = {contact_id}"),
        lambda cursor: cursor.fetchone(),
        "Contact not found"
    )

@app.get("/invoices")
def fetch_invoices(token: str = Depends(oauth2_scheme)):
    utils_jwt.verify_token(token)
    return fetch(
        (f"SELECT * FROM invoices"),
        lambda cursor: cursor.fetchall(),
        "No invoice found"
    )

@app.get("/invoices/{invoice_id}")
def fetch_invoice(invoice_id: int, token: str = Depends(oauth2_scheme)):
    utils_jwt.verify_token(token)
    return fetch(
        (f"SELECT * FROM invoices WHERE id = {invoice_id}"),
        lambda cursor: cursor.fetchone(),
        "Invoice not found"
    )
