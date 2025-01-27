import os
import utils_db
import xmlrpc.client

from dotenv import load_dotenv
from models import Contact, Invoice

def odooToDB():
    load_dotenv()

    url = os.getenv('ODOO_URL')
    db = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USER')
    password = os.getenv('ODOO_PASSWORD')

    # Fetch contacts and invoices from Odoo
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    contact_set = models.execute_kw(
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
    invoice_set = models.execute_kw(
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

    # Ensure tables exist
    utils_db.create_tables()

    # Fetch existing contact IDs from the database
    contact_table_ids = utils_db.get_ids(Contact)
    invoice_table_ids = utils_db.get_ids(Invoice)

    # Fetch contact IDs from the scrapped data
    contact_set_ids = {contact['id'] for contact in contact_set}
    invoice_set_ids = {invoice['id'] for invoice in invoice_set}

    # Insert, update or delete contacts and invoices
    for contact in contact_set:
        utils_db.create_or_update(Contact, contact)

    for contact in contact_table_ids:
        if contact not in contact_set_ids:
            utils_db.delete(Contact, contact)

    for invoice in invoice_set:
        invoice['user_id'] = invoice['user_id'][0]
        invoice['partner_id'] = invoice['partner_id'][0]
        utils_db.create_or_update(Invoice, invoice)

    for invoice in invoice_table_ids:
        if invoice not in invoice_set_ids:
            utils_db.delete(Invoice, invoice)

if __name__ == '__main__':
    odooToDB()
