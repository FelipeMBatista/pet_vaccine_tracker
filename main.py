from datetime import date, timedelta

from client import Client
import sheets

import urllib.parse

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

def start_the_reminders(clients, gsheets):
    """
    Function responsible for starting reminders. She walks through the array of customers checking how many doses their
    pets have and makes the appropriate decision based on the information.

    :param clients: Array containing all customers present in the vaccination sheet.
    :param gsheets: Google Sheets (sheets.py) Object
    """

    for client in clients:
        if client.dose == 1:
            if TODAY <= (client.vaccine_date + timedelta(days=23)) and TODAY >= (client.vaccine_date + timedelta(days=23, weeks=-1)):
                """
                If today is within one week before the final date of the first dose...
        
                The idea is that today is one week before the customer's first dose is due.
                """

                # Message that will be sent to the customer. This message will be embedded in the WhatsApp message link.
                msg = (f"Bom dia {client.name.split()[0].title()}, tudo bem? Aqui é da {PETSHOP_NAME} e estou entrando em "
                       f"contato para lembrar da segunda dose da vacina do seu pet {client.pet_name.title()} que vence "
                       f"dentro de uma semana.\n\nCaso queira marcar a vacina, só nos avisar, ok?")
                wpp_msg = urllib.parse.quote(msg) # Transforming into a url encoding
                wpp_msg_link = f"wa.me/+55{client.phone}?text={wpp_msg}"
                gsheets.update_cell_value(client.row_number, wpp_msg_link)


        elif client.dose == 2:
            if TODAY <= (client.vaccine_date + timedelta(days=358)) and TODAY >= (client.vaccine_date + timedelta(days=358, weeks=-1)):
                """
                If today is within one week before the annual revaccination...

                The idea is that today is one week before the annual revaccination.
                """

                msg = (f"Bom dia {client.name.split()[0].title()}, tudo bem? Aqui é da {PETSHOP_NAME} e estou entrando em "
                       f"contato para lembrar da renovação da vacina do seu pet {client.pet_name.title()} que vence "
                       f"dentro de uma semana.\n\nCaso queira marcar a vacina, só nos avisar, ok?")
                wpp_msg = urllib.parse.quote(msg)
                wpp_msg_link = f"wa.me/+55{client.phone}?text={wpp_msg}"
                gsheets.update_cell_value(client.row_number, wpp_msg_link)
        else:
            """
            If the dose value is not identified, a more "Generic" reminder will be sent.
            """
            msg = (f"Bom dia {client.name.split()[0].title()}, tudo bem? Aqui é da {PETSHOP_NAME} e estou entrando em "
                   f"contato para lembrar de verificar a vacinação do seu pet {client.pet_name.title()}."
                   f"Nossas anotações indicam que está quase na data de revacinar."
                   f"\n\nCaso queira marcar a vacina, só nos avisar, ok?")
            wpp_msg = urllib.parse.quote(msg)
            wpp_msg_link = f"wa.me/+55{client.phone}?text={wpp_msg}"
            gsheets.update_cell_value(client.row_number, wpp_msg_link)


# -------------------------------------------------------------------------------------------------------------------- #


def main():
    # Instantiating the Google sheets class.
    google_sheets = sheets.Sheets(SCOPES, SPREADSHEET_ID, RANGE_NAME)
    google_sheets.login()
    google_sheets.build()
    values = google_sheets.read_sheet() # Receiving the values from the spreadsheet.

    clients = []
    index = 2 # Start in 1 because i have 2 fixed lines
    for row in values[2::]:
        """
        Here we walk through the lines of the spreadsheet. Starting with the second line as the first is the "Header".

        Its columns will be stored separately so that the values can later be used for client instantiation.
        """
        # print(row)
        if not row[0]:  # Verificar se a linha está vazia
            continue  # Pular para a próxima iteração se a linha estiver vazia

        name = row[0]
        pet_name = row[1]
        vaccine_date = date(int(row[2][6::]), int(row[2][3:5]), int(row[2][:2]))
        dose = int(row[3])
        brand = row[4]
        phone = int(row[5])
        new_client = Client(
            name=name,
            pet_name=pet_name,
            vaccine_date=vaccine_date,
            dose=dose,
            brand=brand,
            phone=phone,
            row_number=index
        )
        clients.append(new_client)
        index += 1

    start_the_reminders(clients, google_sheets) # Starting reminders...


if __name__ == "__main__":
    main()