import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Sheets():
    def __init__(self, scopes, spreadsheets_id, range_name):
        self.scopes = scopes,
        self.spreadsheets_id = spreadsheets_id,
        self.range_name = range_name
        # Authentication
        self.creds = None

    def login(self):
        # Checking if the token already exists.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def read_sheet(self):
        try:
            service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.batchUpdate(spreadsheetId=self.spreadsheets_id, body=self.range_name)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                print("No data found")
                return

            print("Column, Column")
            print(values)

        except HttpError as err:
            print(err)