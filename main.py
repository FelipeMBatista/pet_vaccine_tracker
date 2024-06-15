from datetime import date, timedelta
from vaccine_tracker import Vaccine_tracker
import os
from dotenv import load_dotenv

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = [os.getenv("SCOPE")]
# The ID and page (range) of a sample spreadsheet.
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = os.getenv("RANGE_NAME")
PETSHOP_NAME = os.getenv("PETSHOP_NAME")

# Saving the actual date
TODAY = date.today()


def main():
    vaccine_tracker = Vaccine_tracker(scopes=SCOPES,
                                      spreadsheet_id=SPREADSHEET_ID,
                                      range_name=RANGE_NAME,
                                      petshop_name=PETSHOP_NAME,
                                      )
    vaccine_tracker.vaccine_start()


if __name__ == "__main__":
    main()