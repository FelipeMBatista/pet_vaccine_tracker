import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Sheets:
    # Class designed to create a connection with the GoogleSheets API

    def __init__(self, scopes, spreadsheet_id, range_name):
        self.scopes = scopes
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.global_path = os.path.dirname(os.path.realpath(__file__))
        self.credentials_path = os.path.join(self.global_path, 'credentials.json')
        self.token_path = os.path.join(self.global_path, 'token.json')
        # Authentication
        self.creds = None
        # Build
        self.service = None
        self.sheet_id = None
        self.sheet = None

    def login(self):
        # Checking if the token already exists.
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scopes
                )
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def build(self):
        # Starting the service
        self.service = build("sheets", "v4", credentials=self.creds)

        # Get the sheet ID based on the sheet name
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        self.sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheet = self.service.spreadsheets().values()

    def get_all_values(self):
        # Get the values of all cells in the sheet
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name
        ).execute()

        values = result.get('values', [])

        return values

    def read_sheet(self):
        try:
            values = self.get_all_values()

            if not values:
                print("No data found")
                return

            return values

        except HttpError as err:
            print(err)

    def update_cell_value(self, row_number, new_value):
        # Update the value of the cell in the specified row and column
        cell_range = f"{self.range_name}!G{row_number + 1}"
        body = {
            "values": [[new_value]]
        }
        self.sheet.update(spreadsheetId=self.spreadsheet_id, range=cell_range,
                          valueInputOption="USER_ENTERED", body=body).execute()

        self.green_color(row_number)

    def green_color(self, row_number):
        # Set the cell color
        color = {
            "red": 0.7,  # Valor entre 0 e 1
            "green": 1.0,
            "blue": 0.7,
        }

        # Build the update request
        request = {
            "updateCells": {
                "range": {
                    "sheetId": self.sheet_id,  # Usar o sheet_id obtido anteriormente
                    "startRowIndex": row_number,  # Índice da linha da célula
                    "startColumnIndex": 6,  # Índice da coluna inicial da linha
                },
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredFormat": {
                                    "backgroundColor": color,
                                }
                            }
                        ]
                    }
                ],
                "fields": "userEnteredFormat.backgroundColor",
            }
        }

        # Send the update request
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "requests": [request]
            }
        ).execute()
