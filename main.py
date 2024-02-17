from datetime import date, timedelta
from client import Client
import smtplib, ssl
import sheets
import urllib.parse

# If modifying these scopes, delete the file token.json.
SCOPES = "https://www.googleapis.com/auth/spreadsheets"

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1h-WbK4T6rUvD7eUoIO5tBE3pQjxSxrGiKWLpY4lKuEQ"
RANGE_NAME = "2024"

today = date.today()

# Create a secure SSL context
context = ssl.create_default_context()

def main():
    google_sheets = sheets.Sheets(SCOPES, SPREADSHEET_ID, RANGE_NAME)
    google_sheets.login()
    values = google_sheets.read_sheet()

    clients = []
    for row in values[1::]:
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
            phone=phone
        )
        clients.append(new_client)
# ------------------------------------------------------------------------------------------ #
    def email_server(message):
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = "felipemenegasbatista08@gmail.com"
        password = "ckil mrnr ehrh vgln"
        receiver_email = "felipembatista08@gmail.com"
        message = message

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()

    def check_date(clients):
        for client in clients:
            if client.dose == 1:
                if today + timedelta(days=7) == client.vaccine_date + timedelta(days=30):
                    query = f"""\
                    Bom dia {client.name}, aqui é da RuralPet e estou entrando em contato para lembrar da segunda dose\
                     da vacina do seu pet {client.pet_name} que vence dentro de uma semana.
                    """

                    mail_message = f"""\
                    subject: Lembrete segunda dose {client.name}
                    
                    Cliente: {client.name}
                    Pet: {client.pet_name}
                    Data da primeira dose: {client.vaccine_date}
                    Marca da vacina aplicada: {client.vaccine_date}
                    
                    wa.me/+55{client.phone}?text={urllib.parse.quote(query)}
                    """
                    email_server(mail_message)
            elif client.dose == 2:
                if today + timedelta(days=365) == client.vaccine_date + timedelta(days=358):
                    print(f"Renovação anual:"
                          f"\nCliente: {client.name},"
                          f"\nNome do Pet: {client.pet_name},"
                          f"\nData para segunda dose: {client.vaccine_date + timedelta(days=365)}"
                          f"\n\n")

    check_date(clients)

if __name__ == "__main__":
    main()