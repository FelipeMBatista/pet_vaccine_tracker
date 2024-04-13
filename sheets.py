import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Sheets():
    """
    Class designed to create a connection with the GoogleSheets API
    """
    def __init__(self, scopes, spreadsheet_id, range_name):
        self.scopes = scopes
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        # Authentication
        self.creds = None
        # Build
        self.service = None

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

    def build(self):
        # Starting the service
        self.service = build("sheets", "v4", credentials=self.creds)

    def read_sheet(self):
        try:
            self.service = build("sheets", "v4", credentials=self.creds)
            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.range_name).execute()
            values = result.get("values", [])

            if not values:
                print("No data found")
                return

            return values

        except HttpError as err:
            print(err)

    def yellow_color(self):
        # Definir a cor da célula
        color = {
            "red": 0.7,  # Valor entre 0 e 1
            "green": 1.0,
            "blue": 0.7,
        }

        # Obter o ID da planilha com base no nome da planilha
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']

        # Montar a solicitação de atualização
        request = {
            "updateCells": {
                "range": {
                    "sheetId": sheet_id,  # Usar o sheet_id obtido anteriormente
                    "startRowIndex": 2,  # Índice da linha da célula
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

        # Enviar a solicitação de atualização
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "requests": [request]
            }
        ).execute()

        print("Cor da linha atualizada com sucesso!")