from dotenv import load_dotenv
import os
import utils
import xmlrpc.client

def odooToDB():
    load_dotenv()

    conn =  utils.get_psql_conn()

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
    # TODO: data validation
    # print(json.dumps(sorted(list(contact_set), key=lambda x: x['id']), indent=4))
    # print(json.dumps(sorted(list(invoice_set), key=lambda x: x['id']), indent=4))

    # Ensure tables exist
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS contacts (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), phone VARCHAR(255), mobile VARCHAR(255), contact_address TEXT, is_company BOOLEAN)")
    cursor.execute("CREATE TABLE IF NOT EXISTS invoices (id SERIAL PRIMARY KEY, name VARCHAR(255), user_id INTEGER, partner_id INTEGER, date DATE, invoice_date_due DATE, amount_total FLOAT)")
    conn.commit()

    # Fetch existing contact IDs from the database
    cursor.execute("SELECT id FROM contacts")
    contact_table_ids = {row[0] for row in cursor.fetchall()}
    cursor.execute("SELECT id FROM invoices")
    invoice_table_ids = {row[0] for row in cursor.fetchall()}

    # Fetch contact IDs from the scrapped data
    contact_set_ids = {contact['id'] for contact in contact_set}
    invoice_set_ids = {invoice['id'] for invoice in invoice_set}

    # Insert, update or delete contacts and invoices
    for contact in contact_set:
        if not contact['id'] in contact_table_ids:
            print("Inserting contact", contact['id'])
            cursor.execute(
                "INSERT INTO contacts (id, name, email, phone, mobile, contact_address, is_company) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (contact['id'], contact['name'], contact['email'], contact['phone'], contact['mobile'], contact['contact_address'], contact['is_company'])
            )
        #TODO: check if the contact has changed
        else:
            print("Updating contact", contact['id'])
            cursor.execute(
                "UPDATE contacts SET name = %s, email = %s, phone = %s, mobile = %s, contact_address = %s, is_company = %s WHERE id = %s",
                (contact['name'], contact['email'], contact['phone'], contact['mobile'], contact['contact_address'], contact['is_company'], contact['id'])
            )

    for contact in contact_table_ids:
        if contact not in contact_set_ids:
            print("Deleting contact", contact)
            cursor.execute("DELETE FROM contacts WHERE id = %s", (contact,))

    for invoice in invoice_set:
        if not invoice['id'] in invoice_table_ids:
            print("Inserting invoice", invoice['id'])
            cursor.execute(
                "INSERT INTO invoices (id, name, user_id, partner_id, date, invoice_date_due, amount_total) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (invoice['id'], invoice['name'], invoice['user_id'][0], invoice['partner_id'][0], invoice['date'], invoice['invoice_date_due'], invoice['amount_total'])
            )
        #TODO: check if the contact has changed
        else:
            print("Updating invoice", invoice['id'])
            cursor.execute(
                "UPDATE invoices SET name = %s, user_id = %s, partner_id = %s, date = %s, invoice_date_due = %s, amount_total = %s WHERE id = %s",
                (invoice['name'], invoice['user_id'][0], invoice['partner_id'][0], invoice['date'], invoice['invoice_date_due'], invoice['amount_total'], invoice['id'])
            )

    for invoice in invoice_table_ids:
        if invoice not in invoice_set_ids:
            print("Deleting invoice", invoice)
            cursor.execute("DELETE FROM invoices WHERE id = %s", (invoice,))

    # Commit the changes, close the cursor and the connection
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    odooToDB()
