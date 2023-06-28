import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import sessionmaker
from db.models import Email
from db.crud import bulk_create_emails


class TestDBCrud(unittest.TestCase):
    def setUp(self):
        # Create a mock session object
        self.session = MagicMock(spec=sessionmaker())

    def test_bulk_create_emails(self):
        # Define the mock email data
        mock_emails_data = [
            {
                "email_id": "email_id_1",
                "subject": "Subject 1",
                "sender": "sender1@example.com",
                "recipient": "recipient1@example.com",
                "received_date": None,
            },
            {
                "email_id": "email_id_2",
                "subject": "Subject 2",
                "sender": "sender2@example.com",
                "recipient": "recipient2@example.com",
                "received_date": None,
            },
        ]

        # Call the bulk_create_emails method
        bulk_create_emails(self.session, mock_emails_data)

        # Ensure that the session's bulk_save_objects and commit methods were called with the correct arguments
        self.session.bulk_save_objects.assert_called_once_with(
            [Email(**mock_emails_data[0]), Email(**mock_emails_data[1])]
        )
        self.session.commit.assert_called_once()

        # Ensure that the session's close method was called
        self.session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
