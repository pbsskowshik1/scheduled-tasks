import os
from twilio.http.http_client import TwilioHttpClient
from requests import *
from twilio.rest import Client

api_key = os.environ.get("OWM_API_KEY")
api_t = os.environ.get("TWILIO_ACCOUNT_SID")
api_pas = os.environ.get("TWILIO_AUTH_TOKEN")

parameters = {
        "lat" : 13.113587,
        "lon" : 77.568681,
        "appid" : api_key,
        "cnt" : 4,
    }

response = get("https://api.openweathermap.org/data/2.5/forecast",
                params=parameters)
response.raise_for_status()
weather_data = response.json()

will_rain = False

for item in weather_data["list"]:
    condition_code = item["weather"][0]["id"]
    if int(condition_code) <= 700:
        will_rain = True
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(api_t, api_pas, http_client=proxy_client)
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body="It's going to rain today. Remember to bring an umbrella",
        to="whatsapp:+918296082198"
    )
