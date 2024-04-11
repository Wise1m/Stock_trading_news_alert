import requests
import smtplib
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


EMAIL = "aribisalapraise12@gmail.com"
PASSWORD = "iickvvwjhumnwcvj"
api_key = "ad1b41b60169d4b3aa34c3bea6a072bc"
account_sid = 'ACc0791c7a285a7207aa839809d402118f'
auth_token = '421c46b2f56fe04a32e4a753d619611a'

api_endpoint = "https://api.openweathermap.org/data/3.0/onecall"
parameters = {
    "lat": 7.257132,
    "lon": 5.205791,
    "exclude": "current,minutely,daily",
    "appid": api_key,

}

response = requests.get(api_endpoint, params=parameters)
response.raise_for_status()
data = response.json()

will_rain = False
hourly = data["hourly"][:12]
for weather in hourly:
    weather_code = weather["weather"][0]["id"]
    if int(weather_code) < 700:
        will_rain = True

if will_rain:
    msg = "Bring an umbrella with you today"

    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    # with smtplib.SMTP("smtp.gmail.com", 587) as server:
    #     server.starttls()
    #     server.login(EMAIL, PASSWORD)
    #     server.sendmail(
    #         from_addr=EMAIL,
    #         to_addrs="praisearibisala3@gmail.com",
    #         msg=f"Subject: Reminder!!!\n\n{msg}"
    #     )

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body=msg,
        from_='+13344234161',
        to='+2348168021158'
    )
    print(message.status)

