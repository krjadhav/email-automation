from db.setup import DatabaseSetup
from gmail_api.gmail_auth import GmailAuth
from gmail_api.gmail_fetch import GmailFetchEmail

if __name__ == "__main__":
    # Authenticate to Gmail API
    auth = GmailAuth()

    # Fetch emails from Gmail API
    fetched_emails = GmailFetchEmail(auth.service).fetch_emails()

    # Store fetched emails in the database
    db = DatabaseSetup()

    # Load rules from JSON file

    # Process emails based on rules
