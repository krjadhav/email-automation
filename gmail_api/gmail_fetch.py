import datetime

from googleapiclient.discovery import build


class GmailFetchEmail:
    def __init__(self, service):
        self.service = service

    def fetch_emails(self):
        # Fetch a list of emails from the Inbox label
        results = self.service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        emails = results.get("messages", [])

        fetched_emails = []

        if not emails:
            raise Exception("No emails found!")

        for email in emails:
            # Fetch individual email details
            email_data = (
                self.service.users()
                .messages()
                .get(userId="me", id=email["id"], format="full")
                .execute()
            )

            # Extract subject, from, and to fields
            headers = email_data["payload"]["headers"]
            subject = self.get_header_value(headers, "Subject")
            sender = self.get_header_value(headers, "From")
            recipient = self.get_header_value(headers, "To")
            received_timestamp = (
                int(email_data["internalDate"]) / 1000
            )  # Convert milliseconds to seconds
            received_date = datetime.datetime.fromtimestamp(received_timestamp)

            # Create a dictionary with the email details
            email_details = {
                "email_id": email["id"],
                "subject": subject,
                "sender": sender,
                "recipient": recipient,
                "received_date": received_date,
            }
            fetched_emails.append(email_details)

        return fetched_emails

    @staticmethod
    def get_header_value(headers, name):
        for header in headers:
            if header["name"] == name:
                return header["value"]
        return ""

    def fetch_labels(self):
        labels = self.service.users().labels().list(userId="me").execute().get("labels", [])
        for label in labels:
            print(label["name"])
