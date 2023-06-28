import unittest
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from gmail_auth import GmailAuth


class TestGmailAuth(unittest.TestCase):
    def test_authenticate(self):
        # Create an instance of the GmailAuth class
        gmail_auth = GmailAuth()

        # Ensure that credentials and service are set correctly
        self.assertIsNotNone(gmail_auth.creds)
        self.assertIsInstance(gmail_auth.creds, Credentials)
        self.assertIsNotNone(gmail_auth.service)
        self.assertIsInstance(gmail_auth.service, build)

        # Check if token.json file exists
        self.assertTrue(os.path.exists("secrets/token.json"))

    def test_authenticate_with_existing_credentials(self):
        # Create an instance of the GmailAuth class
        gmail_auth = GmailAuth()

        # Save the existing credentials to a temporary file
        temp_token_path = "secrets/temp_token.json"
        with open(temp_token_path, "w") as token_file:
            token_file.write(gmail_auth.creds.to_json())

        # Create a new instance of the GmailAuth class
        new_gmail_auth = GmailAuth()

        # Ensure that the new instance uses the existing credentials
        self.assertIsNotNone(new_gmail_auth.creds)
        self.assertIsInstance(new_gmail_auth.creds, Credentials)
        self.assertEqual(gmail_auth.creds.valid, new_gmail_auth.creds.valid)

        # Delete the temporary token file
        os.remove(temp_token_path)


if __name__ == "__main__":
    unittest.main()
