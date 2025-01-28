# OdooToDB

## Overview
This project is designed to expose contacts and invoices from an Odoo instance via an API. It consists of an API server and a cron job that fetches data from the Odoo instance and updates a database accordingly.

## Features
* A cron job regularly updates the database with data from the Odoo instance.
* Provides access to data via a FastAPI-based API.
* Includes authentication using JWT (JSON Web Tokens).

## Requirements
* A running Odoo instance
* A PostgreSQL database ready to accept data
* A server application (e.g., Uvicorn)
* Python and pip

## Running Locally
1. Clone the repository.
2. Navigate to the `src/` directory.
3. Create a `.env` file with the following variables:
    ```env
    PSQL_DB=<db_name>
    PSQL_HOSTNAME=<postgres_hostname>
    PSQL_PROXY_PORT=<postgres_port>
    PSQL_USER=<postgres_user>
    PSQL_PASSWORD=<postgres_password>
    ODOO_URL=https://<your_odoo_instance_name>.odoo.com
    ODOO_DB=<your_odoo_database_name>
    ODOO_USER=<your_odoo_username>
    ODOO_PASSWORD=<your_odoo_password>
    JWT_SECRET_KEY=<any_secret_key>
    JWT_ALGORITHM=<any_jwt_algorithm>
    JWT_EXPIRATION_MINUTES=<token_validity_duration_in_minutes>
    ```
4. Install the dependencies:
    ```bash
    pip install --no-cache-dir -r src/requirements.txt
    ```
5. Run the application using two separate terminals:
    - **Terminal 1:** Start the API server:
      ```bash
      uvicorn server:app --host 0.0.0.0 --port 8000
      ```
    - **Terminal 2:** Start the cron job:
      ```bash
      python3 cron.py
      ```

## API Endpoints

### Authentication

* **POST /token**
    - Authenticates a user and returns an access token.
    - Requires `username` and `password` in the request body.
    - Example response:
      ```json
      {
          "access_token": "your_jwt_token",
          "token_type": "bearer"
      }
      ```

### Contacts

* **GET /contacts**
    - Fetches all contacts from the database.
    - Requires a valid JWT token in the `Authorization` header.
    - Example response:
      ```json
      [
          {
              "id": 1,
              "name": "John Doe",
              "email": "john.doe@example.com",
              "phone": "123-456-7890",
              "mobile": "555-123-4567",
              "contact_address": "123 Main St, Springfield, USA",
              "is_company": false
          },
          {
              "id": 2,
              "name": "Jane Smith",
              "email": "jane.smith@example.com",
              "phone": "987-654-3210",
              "mobile": "555-987-6543",
              "contact_address": "456 Elm St, Springfield, USA",
              "is_company": true
          }
      ]
      ```

* **GET /contacts/{contact_id}**
    - Fetches a single contact by its ID.
    - Requires a valid JWT token in the `Authorization` header.
    - Example response:
      ```json
      {
          "id": 1,
          "name": "John Doe",
          "email": "john.doe@example.com",
          "phone": "123-456-7890",
          "mobile": "555-123-4567",
          "contact_address": "123 Main St, Springfield, USA",
          "is_company": false
      }
      ```

### Invoices

* **GET /invoices**
    - Fetches all invoices from the database.
    - Requires a valid JWT token in the `Authorization` header.
    - Example response:
      ```json
      [
          {
              "id": 1,
              "name": "INV-001",
              "user_id": 101,
              "partner_id": 201,
              "date": "2023-10-01",
              "invoice_date_due": "2023-10-15",
              "amount_total": 1500.00
          },
          {
              "id": 2,
              "name": "INV-002",
              "user_id": 102,
              "partner_id": 202,
              "date": "2023-10-05",
              "invoice_date_due": "2023-10-20",
              "amount_total": 2000.00
          }
      ]
      ```

* **GET /invoices/{invoice_id}**
    - Fetches a single invoice by its ID.
    - Requires a valid JWT token in the `Authorization` header.
    - Example response:
      ```json
      {
          "id": 1,
          "name": "INV-001",
          "user_id": 101,
          "partner_id": 201,
          "date": "2023-10-01",
          "invoice_date_due": "2023-10-15",
          "amount_total": 1500.00
      }
      ```

## Security

- **Authentication**: The API uses JWT for secure authentication. Users must provide a valid token in the `Authorization` header for all endpoints except `/token`.
- **Password Handling**: User passwords are hashed using bcrypt before storage, ensuring sensitive data remains secure.

## Example Workflow
1. Add a user manually to the `users` table in your database to enable authentication.
2. Authenticate using `/token` to receive an access token:
    ```bash
    curl -X POST "<base_url>/token" -d "username=<my_username>&password=<my_password>"
    ```
3. Use the access token to make authorized requests to endpoints like `/contacts` or `/invoices`:
    ```bash
    curl -X GET "<base_url>/contacts" -H "Authorization: Bearer <received_token>"
    ```
