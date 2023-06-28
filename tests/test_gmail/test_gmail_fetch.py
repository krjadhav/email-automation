import unittest
from unittest.mock import MagicMock
from gmail_fetch import GmailFetchEmail


class TestGmailFetchEmail(unittest.TestCase):
    def setUp(self):
        # Create a mock service object
        self.service = MagicMock()

        # Create an instance of the GmailFetchEmail class with the mock service
        self.gmail_fetch_email = GmailFetchEmail(self.service)

    def test_fetch_emails(self):
        # Define the mock results and email data
        mock_results = {
            "messages": [{"id": "email_id_1"}, {"id": "email_id_2"}, {"id": "email_id_3"}]
        }
        mock_email_data = {
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Example Subject"},
                    {"name": "From", "value": "example@example.com"},
                    {"name": "To", "value": "recipient@example.com"},
                ]
            },
            "internalDate": "1625101552000",  # Mocked received timestamp
        }

        # Mock the service's users().messages().list().execute() method to return the mock results
        self.service.users().messages().list().execute.return_value = mock_results

        # Mock the service's users().messages().get().execute() method to return the mock email data
        self.service.users().messages().get().execute.return_value = mock_email_data

        # Call the fetch_emails method
        fetched_emails = self.gmail_fetch_email.fetch_emails()

        # Ensure that the service's users().messages().list() method was called with the correct arguments
        self.service.users().messages().list.assert_called_once_with(
            userId="me", labelIds=["INBOX"]
        )
        # Ensure that the service's users().messages().get() method was called for each email ID
        self.service.users().messages().get.assert_any_call(
            userId="me", id="email_id_1", format="full"
        )
        self.service.users().messages().get.assert_any_call(
            userId="me", id="email_id_2", format="full"
        )
        self.service.users().messages().get.assert_any_call(
            userId="me", id="email_id_3", format="full"
        )

        # Ensure that the fetched_emails list contains the expected email details
        expected_emails = [
            {
                "email_id": "email_id_1",
                "subject": "Example Subject",
                "sender": "example@example.com",
                "recipient": "recipient@example.com",
                "received_date": datetime.datetime.fromtimestamp(1625101552),
            },
            # Repeat for other emails
        ]
        self.assertEqual(fetched_emails, expected_emails)

    def test_get_header_value(self):
        # Define the mock headers
        mock_headers = [
            {"name": "Subject", "value": "Example Subject"},
            {"name": "From", "value": "example@example.com"},
            {"name": "To", "value": "recipient@example.com"},
        ]

        # Call the get_header_value method for each header name
        subject = self.gmail_fetch_email.get_header_value(mock_headers, "Subject")
        sender = self.gmail_fetch_email.get_header_value(mock_headers, "From")
        recipient = self.gmail_fetch_email.get_header_value(mock_headers, "To")

        # Ensure that the correct header values are returned
        self.assertEqual(subject, "Example Subject")
        self.assertEqual(sender, "example@example.com")
        self.assertEqual(recipient, "recipient@example.com")

        # Call the get_header_value method with a non-existent header name
        non_existent_header = self.gmail_fetch_email.get_header_value(mock_headers, "Nonexistent")
        # Ensure that an empty string is returned for the non-existent header
        self.assertEqual(non_existent_header, "")

    def test_fetch_labels(self):
        # Define the mock labels
        mock_labels = [{"name": "Label 1"}, {"name": "Label 2"}, {"name": "Label 3"}]

        # Mock the service's users().labels().list().execute() method to return the mock labels
        self.service.users().labels().list().execute.return_value = {"labels": mock_labels}

        # Redirect the print function to a buffer
        import sys
        from io import StringIO

        buffer = StringIO()
        sys.stdout = buffer

        # Call the fetch_labels method
        self.gmail_fetch_email.fetch_labels()

        # Ensure that the service's users().labels().list() method was called with the correct arguments
        self.service.users().labels().list.assert_called_once_with(userId="me")

        # Ensure that the labels were printed
        expected_output = "Label 1\nLabel 2\nLabel 3\n"
        self.assertEqual(buffer.getvalue(), expected_output)

        # Restore the original print function
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
