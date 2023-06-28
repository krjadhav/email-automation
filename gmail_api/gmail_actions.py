class GmailActions:
    def __init__(self, service):
        self.service = service

    def mark_email_as_read(self, email_id):
        # Modify the email's "read" label
        self.service.users().messages().modify(
            userId="me", id=email_id, body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    def mark_email_as_unread(self, email_id):
        # Modify the email's "unread" label
        self.service.users().messages().modify(
            userId="me", id=email_id, body={"addLabelIds": ["UNREAD"]}
        ).execute()

    def move_email_to_label(self, email_id, label_id):
        # Move the email to the specified label
        self.service.users().messages().modify(
            userId="me", id=email_id, body={"addLabelIds": [label_id]}
        ).execute()
