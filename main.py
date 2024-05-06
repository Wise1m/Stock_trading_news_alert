import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

alphavantage_api_endpoint = "https://www.alphavantage.co/query"
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_API_KEY,
}

response = requests.get(alphavantage_api_endpoint, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [val for (key, val) in data.items()]
closing_price_yesterday = float(data_list[0]["4. close"])
closing_price_day_before_yesterday = float(data_list[1]["4. close"])

# Calculating percentage change
percentage = int((closing_price_yesterday / closing_price_day_before_yesterday) * 100)
percentage_change = percentage - 100
if percentage_change > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(percentage_change) >= 2:
    newsapi_api_endpoint = "https://newsapi.org/v2/everything"
    newsapi_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWSAPI_API_KEY,
    }
    news_response = requests.get(newsapi_api_endpoint, params=newsapi_parameters)
    news_response.raise_for_status()

    news = news_response.json()["articles"]
    three_articles = news[:3]
    articles = [f"{STOCK}: {up_down}{percentage_change}%\nHeadline: {article["title"]}. \nBrief: {article["description"]}" for article in three_articles]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in articles:
        message = client.messages.create(
                body=articles,
                from_='+13344234161',
                to='+2348168021158'
        )
