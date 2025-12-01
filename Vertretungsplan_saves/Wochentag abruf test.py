import datetime

heute = datetime.date.today()
Wochentag = heute.strftime("%A")

if Wochentag == "Monday":
    print("Montag")