# Email Automation System

The Email Automation System is a Python application that allows you to automate email processing based on predefined rules. It integrates with the Gmail API and a PostgreSQL database to fetch emails, apply rules, and perform actions on the emails.

## Features

- Fetch emails from the Gmail inbox label using the Gmail API.
- Define rules to filter and process emails based on various criteria such as sender, recipient, subject, and received date.
- Apply actions on the matched emails, such as marking as read, marking as unread, and moving to a specific label/folder.
- Store email data in a PostgreSQL database for efficient retrieval and management.
- Use SQLAlchemy as the Object-Relational Mapping (ORM) tool for interacting with the database.
- Use Docker to run the PostgreSQL database in a containerized environment.

## Installation

1. Set up virtual environment and install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:
   - Make sure you have Docker installed on your system.
   - Run the following command to start the PostgreSQL database container:

     ```bash
     docker run --name email-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
     ```

   - The database will be available on `localhost:5432` with the default username (`postgres`) and password (`password`).

4. Configure Gmail API access:
   - Follow the Gmail API Python Quickstart guide to set up your API credentials and enable the Gmail API for your project.
   - Download the `credentials.json` file and place it in the `secrets` folder.

5. Set up environment variables:
   - Create a `.env` file in the `secrets` folder.
   - Define the following environment variables in the `.env` file:

     ```
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=postgres
     DB_USER=postgres
     DB_PASSWORD=password
     ```

6. Run the application:
   - Start the application by running `main.py`:

     ```bash
     python main.py
     ```

## Directory Breakdown

- **main.py**: The main entry point of the application. It initializes the necessary components and starts the email processing.
- **rules.json**: A JSON file that contains the rules for email processing. Each rule specifies conditions and actions to be performed on matching emails.
- **secrets/**: A directory to store sensitive data and configuration files.
  - **credentials.json**: The credentials file for accessing the Gmail API.
  - **token.json**: The token file for authorization with the Gmail API.
  - **.env**: The environment variable file for configuring the database connection.
- **gmail_api/**: A directory that contains the modules related to interacting with the Gmail API.
  - **gmail_auth.py**: The module responsible for authenticating with the Gmail API.
  - **gmail_fetch.py**: The module for fetching emails from the Gmail API.
  - **gmail_actions.py**: The module for performing actions on emails using the Gmail API.
- **db/**: A directory that holds the modules related to database operations.
  - **crud.py**: The module with CRUD (Create, Read, Update, Delete) functions for interacting with the database.
  - **models.py**: The module defining the SQLAlchemy models for the database tables.
  - **setup.py**: The module for setting up the database connection and creating the necessary tables.
- **services/**: A directory containing service modules for specific tasks.
  - **load_rules.py**: The module responsible for loading the rules from the rules.json file.
  - **process_emails.py**: The module for processing emails based on the loaded rules.
- **tests/**: A directory that holds the unit tests for the application.
  - **test_gmail/**: The directory for tests related to the Gmail API modules.
  - **test_db/**: The directory for tests related to the database modules.
  - **test_services/**: The directory for tests related to the service modules.

## Testing

The application includes unit tests to ensure the correctness of its components. To run the tests, use the following command:

```bash
python -m unittest discover tests
```

## Contributing

Contributions to the Email Automation System are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
