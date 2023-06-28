from db.crud import read_email_from_db


def process_emails(service, session, rules):
    gmail_action = GmailActions(service)
    for rule in rules:
        emails = read_email_from_db(session, rule)
        # for action in rule["actions"]:
        #     folder = action.get("folder", "")
        #     process_action(gmail_action, action, emails, folder)
