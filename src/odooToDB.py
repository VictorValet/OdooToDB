import os
import utils_db
import xmlrpc.client

from dotenv import load_dotenv
from models import Contact, Invoice

def getContactSet(db, uid, password, models):
    return models.execute_kw(
        db,
        uid,
        password,
        'res.partner',
        'search_read',
        [[]],
        {'fields': [
            'id',
            'name',
            'email',
            'phone',
            'mobile',
            'contact_address',
            'is_company'
    ]})

def getInvoiceSet(db, uid, password, models):
    return models.execute_kw(
        db,
        uid,
        password,
        'account.move',
        'search_read',
        [[]],
        {'fields': [
            'id',
            'name',
            'user_id',
            'partner_id',
            'date',
            'invoice_date_due',
            'amount_total'
    ]})

def createOrUpdateItems(contact_set, invoice_set):
    for contact in contact_set:
        utils_db.create_or_update(Contact, contact)
    for invoice in invoice_set:
        invoice['user_id'] = invoice['user_id'][0]
        invoice['partner_id'] = invoice['partner_id'][0]
        utils_db.create_or_update(Invoice, invoice)

def deleteItems(contact_set, invoice_set):
    contact_ids_db = utils_db.get_ids(Contact)
    invoice_ids_db = utils_db.get_ids(Invoice)
    contact_ids_odoo = {contact['id'] for contact in contact_set}
    invoice_ids_odoo = {invoice['id'] for invoice in invoice_set}

    for contact in contact_ids_db:
        if contact not in contact_ids_odoo:
            utils_db.delete(Contact, contact)
    for invoice in invoice_ids_db:
        if invoice not in invoice_ids_odoo:
            utils_db.delete(Invoice, invoice)

def main():
    load_dotenv()
    url = os.getenv('ODOO_URL')
    db = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USER')
    password = os.getenv('ODOO_PASSWORD')

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    contact_set = getContactSet(db, uid, password, models)
    invoice_set = getInvoiceSet(db, uid, password, models)
    createOrUpdateItems(contact_set, invoice_set)
    deleteItems(contact_set, invoice_set)

if __name__ == '__main__':
    main()
