from db.crud import bulk_create_emails
from db.setup import DatabaseSetup
from gmail_api.gmail_auth import GmailAuth
from gmail_api.gmail_fetch import GmailFetchEmail
from services.load_rules import load_rules


if __name__ == "__main__":
    # Authenticate to Gmail API
    auth = GmailAuth()

    # Fetch emails from Gmail API
    fetched_emails = GmailFetchEmail(auth.service).fetch_emails()

    # Store fetched emails in the database
    db = DatabaseSetup()
    bulk_create_emails(db.session, fetched_emails)

    # Load rules from JSON file
    rules = load_rules("rules.json")

    # Process emails based on rules
