import unittest
from unittest.mock import MagicMock
from db.crud import read_email_from_db
from gmail_api.gmail_actions import GmailActions
from services.process_emails import process_emails, process_action


class TestProcessEmails(unittest.TestCase):
    def setUp(self):
        # Create mock objects for service and session
        self.service = MagicMock()
        self.session = MagicMock()

    def test_process_action_mark_as_read(self):
        # Define the mock action and email data
        mock_action = {"action": "mark_as_read"}
        mock_emails = [
            {"email_id": "email_id_1", "subject": "Subject 1"},
            {"email_id": "email_id_2", "subject": "Subject 2"},
        ]

        # Create a mock GmailActions object
        gmail_action = MagicMock(spec=GmailActions)

        # Call the process_action method
        process_action(gmail_action, mock_action, mock_emails)

        # Ensure that the mark_email_as_read method was called for each email
        gmail_action.mark_email_as_read.assert_called_with("email_id_1")
        gmail_action.mark_email_as_read.assert_called_with("email_id_2")

    def test_process_emails(self):
        # Define the mock rules and email data
        mock_rules = [
            {
                "predicate": "All",
                "conditions": [
                    {"field": "From", "predicate": "contains", "value": "example@example.com"}
                ],
                "actions": [{"action": "mark_as_read"}],
            },
            {
                "predicate": "Any",
                "conditions": [
                    {"field": "Subject", "predicate": "contains", "value": "Important"}
                ],
                "actions": [{"action": "move_to_label", "folder": "Archive"}],
            },
        ]
        mock_emails = [
            {
                "email_id": "email_id_1",
                "subject": "Important Email",
                "sender": "example@example.com",
            },
            {
                "email_id": "email_id_2",
                "subject": "Another Email",
                "sender": "another@example.com",
            },
        ]

        # Create mock objects for GmailActions and read_email_from_db
        gmail_action = MagicMock(spec=GmailActions)
        read_email_from_db_mock = MagicMock(return_value=mock_emails)

        # Mock the read_email_from_db function
        with unittest.mock.patch(
            "services.process_emails.read_email_from_db", read_email_from_db_mock
        ):
            # Call the process_emails method
            process_emails(self.service, self.session, mock_rules)

        # Ensure that the read_email_from_db function was called with the correct arguments
        read_email_from_db_mock.assert_called_with(self.session, mock_rules[0])

        # Ensure that the mark_email_as_read method was called for the relevant emails
        gmail_action.mark_email_as_read.assert_called_with("email_id_1")

        # Ensure that the move_email_to_label method was called for the relevant email
        gmail_action.move_email_to_label.assert_called_with("email_id_1", "Archive")

    # Add more test cases for other scenarios if needed


if __name__ == "__main__":
    unittest.main()
