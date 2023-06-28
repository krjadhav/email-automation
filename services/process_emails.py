from db.crud import read_email_from_db
from gmail_api.gmail_actions import GmailActions


def process_action(gmail_action, rule, emails, label="INBOX"):
    for email in emails:
        email_id = email["email_id"]
        if rule["action"] == "mark_as_read":
            gmail_action.mark_email_as_read(email_id)
            print(f"Marked {email_id} as read")
        elif rule["action"] == "mark_as_unread":
            gmail_action.mark_email_as_unread(email_id)
            print(f"Marked {email_id} as unread")
        elif rule["action"] == "move_to_label":
            gmail_action.move_email_to_label(email_id, label)
            print(f"Moved {email_id} to {label}")


def process_emails(service, session, rules):
    gmail_action = GmailActions(service)
    for rule in rules:
        emails = read_email_from_db(session, rule)
        for action in rule["actions"]:
            folder = action.get("folder", "")
            process_action(gmail_action, action, emails, folder)
