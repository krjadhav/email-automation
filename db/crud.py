from db.models import Email

# Bulk create emails
def bulk_create_emails(session, emails_data):
    emails = [Email(**email_data) for email_data in emails_data]
    session.bulk_save_objects(emails)
    session.commit()
    session.close()
