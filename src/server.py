import bcrypt
import utils_db
import utils_jwt

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import Contact, Invoice

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form : OAuth2PasswordRequestForm = Depends()):
    user = utils_db.get_user_by_username(form.username)
    if user:
        if bcrypt.checkpw(form.password.encode("utf-8"), user.password_hash.encode("utf-8")):
            access_token = utils_jwt.create_access_token(data={"sub": form.username})
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/contacts")
def fetch_contacts(token: str = Depends(oauth2_scheme)):
    utils_jwt.verify_token(token)
    data = utils_db.get(Contact)
    if not data:
        raise HTTPException(status_code=404, detail="No contact found")
    return data

@app.get("/contacts/{contact_id}")
def fetch_contact(contact_id: int, token: str = Depends(oauth2_scheme)):
    utils_jwt.verify_token(token)
    data = utils_db.get(Contact, contact_id)
    if not data:
        raise HTTPException(status_code=404, detail="Contact not found")
    return data[0]

@app.get("/invoices")
def fetch_invoices(token: str = Depends(oauth2_scheme)):
    utils_jwt.verify_token(token)
    data = utils_db.get(Invoice)
    if not data:
        raise HTTPException(status_code=404, detail="No invoice found")
    return data

@app.get("/invoices/{invoice_id}")
def fetch_invoice(invoice_id: int, token: str = Depends(oauth2_scheme)):
    utils_jwt.verify_token(token)
    data = utils_db.get(Invoice, invoice_id)
    if not data:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return data[0]
