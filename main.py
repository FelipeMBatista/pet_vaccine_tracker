from datetime import date, timedelta
from client import Client
from vaccine import Vaccine

today = date.today()

renan = Client(
    "Renan Hug",
    55555555,
    "Jubileu"
)
felipe = Client(
    "Felipe Bat",
    123123123,
    "Jaime Jaquez Junior"
)

vacina1 = Vaccine(renan, date(2024, 1, 12), 1)
vacina2 = Vaccine(renan, date(2024, 2, 12), 2)

def check_date(vaccine):
    if vaccine.dose == 1:
        if today + timedelta(days=7) == vaccine.date + timedelta(days=30):
            return "primeira dose"
    elif vaccine.dose == 2:
        if today + timedelta(days=365) == vaccine.date + timedelta(days=358):
            return "Segunda dose"

print(check_date(vacina2))