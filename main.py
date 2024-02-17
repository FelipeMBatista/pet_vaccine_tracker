from datetime import date, timedelta
from client import Client
from vaccine import Vaccine
import sheets

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = "https://www.googleapis.com/auth/spreadsheets"

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1h-WbK4T6rUvD7eUoIO5tBE3pQjxSxrGiKWLpY4lKuEQ"
RANGE_NAME = "2024"

def main():
    google_sheets = sheets.Sheets(SCOPES, SPREADSHEET_ID, RANGE_NAME)
    google_sheets.login()
    values = google_sheets.read_sheet()

    test = []
    for row in values[1::]:
        # print(row[2][:2])
        # row_date = date(int(row[2][6::]), int(row[2][3:5]), int(row[2][:2]))
        # print(f"Sheet Date {row_date}")
        my_row = row
        my_row[0] = row[0]
        test.append(my_row[0])
    print(test)

    # print(f"Today {date.today()}")

    # today = date.today()
    #
    # renan = Client(
    #     "Renan Hug",
    #     55555555,
    #     "Jubileu"
    # )
    # felipe = Client(
    #     "Felipe Bat",
    #     123123123,
    #     "Jaime Jaquez Junior"
    # )
    #
    # vacina1 = Vaccine(renan, date(2024, 1, 12), 1)
    # vacina2 = Vaccine(renan, date(2024, 2, 12), 2)
    #
    # def check_date(vaccine):
    #     if vaccine.dose == 1:
    #         if today + timedelta(days=7) == vaccine.date + timedelta(days=30):
    #             return "primeira dose"
    #     elif vaccine.dose == 2:
    #         if today + timedelta(days=365) == vaccine.date + timedelta(days=358):
    #             return "Segunda dose"
    #
    # print(check_date(vacina2))

if __name__ == "__main__":
    main()