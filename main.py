import requests
from datetime import datetime
import smtplib
from time import sleep

MY_EMAIL = "your_email@gmail.com"
MY_PASSWORD = "your_password"
MY_LAT = "your latitude"
MY_LONG = "your longitude"
PARAMETERS = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def iss_locator():
    """tracks the iss location and compares it to my current location"""
    # make an api requests for iss location
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # info about my current location through api
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=PARAMETERS)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    # calculate the difference between the iss location and my current position, difference should be within 5 degrees
    if abs(MY_LAT - iss_latitude) <= 5 and abs(MY_LONG - iss_longitude) <= 5:
        if (time_now >= sunset) or (time_now <= sunrise):
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg="Subject:ISS is near!\n\nISS is near and it is currently night time. Look up in the sky."
                )


while True:
    iss_locator()
    sleep(60)
