from datetime import date, timedelta

from client import Client
import sheets

import urllib.parse

from email.message import Message
import smtplib

import os

from dotenv import load_dotenv

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = [os.getenv("SCOPE")]
# The ID and page (range) of a sample spreadsheet.
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = os.getenv("RANGE_NAME")

# If you are not going to use Gmail, change the Server
SMTP_SERVER = "smtp.gmail.com"
PORT = 587  # For starttls

# Saving the actual date
TODAY = date.today()


def send_email(subject, final_msg):
    """
    Function responsible for sending the email. Stores the subject, sender's email,
    recipient's email and sender's password.

    Make an attempt to connect to the Gmail server, log in and finally send the email.

    :param subject: The subject of the email

    :param final_msg: The final message of the email. Embedded messages, such as whatsapp message will come by parameter
    """

    msg = Message()
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_FROM")
    msg['To'] = os.getenv("EMAIL_TO")
    password = os.getenv("SENDER_PASSWORD")

    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(final_msg)

    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.ehlo()  # Can be omitted
        server.starttls()  # Secure the connection
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


def email_message(client, wpp_msg):
    """
    Function responsible for formulating the email subject and message.
    Format the text for your necessary cases, format the date for the local format (in this case Brazil)
    and create the anchor tag responsible for the link for sending the WhatsApp message to the end customer.

    :param client: The client is the object that contains all information about the client,
    their pet and information related to vaccines.

    :param wpp_msg: Parameter responsible for receiving the message that will be embedded in the WhatsApp sending link.
    """

    subject = f"Lembrete de vacinação {client.name.title()}"
    final_msg = f"""\
    <p>Cliente: {client.name}</p>
    <p>Pet: {client.pet_name}</p>
    <p>Data da última dose: {client.vaccine_date.day} / {client.vaccine_date.month} / {client.vaccine_date.year}</p>
    <p>Marca da vacina aplicada: {client.brand}</p>

    <a href=wa.me/+55{client.phone}?text={wpp_msg}>CLIQUE AQUI PARA ENVIAR O LEMBRETE</a>
    """

    send_email(subject, final_msg)


def start_the_reminders(clients):
    """
    Function responsible for starting reminders. She walks through the array of customers checking how many doses their
    pets have and makes the appropriate decision based on the information.

    :param clients: Array containing all customers present in the vaccination sheet.
    """

    for client in clients:
        if client.dose == 1:
            if TODAY + timedelta(days=7) == client.vaccine_date + timedelta(days=30):
                """
                If 7 days from now is equal to 1 month after the first dose...
                
                The idea is that today is one week before the customer's first dose is due.
                """

                # Message that will be sent to the customer. This message will be embedded in the WhatsApp message link.
                msg = (f"Bom dia {client.name.split()[0].title()}, tudo bem? Aqui é da RuralPet e estou entrando em "
                       f"contato para lembrar da segunda dose da vacina do seu pet {client.pet_name.title()} que vence "
                       f"dentro de uma semana.\n\nCaso queira marcar a vacina, só nos avisar, ok?")
                wpp_msg = urllib.parse.quote(msg) # Transforming into a url encoding
                email_message(client, wpp_msg)

        elif client.dose == 2:
            if TODAY == client.vaccine_date + timedelta(days=358):
                """
                If today is equal to 358 days (1 week to close 1 year) since the last dose...

                The idea is that today is 1 week before the annual revaccination.
                """
                msg = (f"Bom dia {client.name.split()[0].title()}, tudo bem? Aqui é da RuralPet e estou entrando em "
                       f"contato para lembrar da renovação da vacina do seu pet {client.pet_name.title()} que vence "
                       f"dentro de uma semana.\n\nCaso queira marcar a vacina, só nos avisar, ok?")
                wpp_msg = urllib.parse.quote(msg)
                email_message(client, wpp_msg)
        else:
            """
            If the dose value is not identified, a more "Generic" reminder will be sent.
            """
            msg = (f"Bom dia {client.name.split()[0].title()}, tudo bem? Aqui é da RuralPet e estou entrando em "
                   f"contato para lembrar de verificar a vacinação do seu pet {client.pet_name.title()}."
                   f"Nossas anotações indicam que está quase na data de revacinar."
                   f"\n\nCaso queira marcar a vacina, só nos avisar, ok?")
            wpp_msg = urllib.parse.quote(msg)
            email_message(client, wpp_msg)


# -------------------------------------------------------------------------------------------------------------------- #


def main():
    # Instantiating the Google sheets class.
    google_sheets = sheets.Sheets(SCOPES, SPREADSHEET_ID, RANGE_NAME)
    google_sheets.login()
    google_sheets.build()
    values = google_sheets.read_sheet() # Receiving the values from the spreadsheet.
    print(f"{values}\n\n")
    google_sheets.yellow_color()

    # clients = []
    # for row in values[1::]:
    #     """
    #     Here we walk through the lines of the spreadsheet. Starting with the second line as the first is the "Header".
    #
    #     Its columns will be stored separately so that the values can later be used for client instantiation.
    #     """
    #     name = row[0]
    #     pet_name = row[1]
    #     vaccine_date = date(int(row[2][6::]), int(row[2][3:5]), int(row[2][:2]))
    #     dose = int(row[3])
    #     brand = row[4]
    #     phone = int(row[5])
    #     new_client = Client(
    #         name=name,
    #         pet_name=pet_name,
    #         vaccine_date=vaccine_date,
    #         dose=dose,
    #         brand=brand,
    #         phone=phone
    #     )
    #     clients.append(new_client)

    # start_the_reminders(clients) # Starting reminders...


if __name__ == "__main__":
    main()