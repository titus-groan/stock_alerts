import os
import requests
from twilio.rest import Client

"""

Don't know how to use environmental variables?
https://www.twilio.com/blog/environment-variables-python
https://www.twilio.com/blog/how-to-set-environment-variables.html

Don't have your own server to run/test this script contonuously? 
Try Anaconda's https://www.pythonanywhere.com/
Note: You'll need to set up new enironmental variables on server

"""

# Use local environmental variables for security reasons (to avoid exposing phone numbers, keys, and IDs) 
VIRTUAL_TWILIO_NUMBER = os.environ["virtual twilio number"]
# Must use a verified number to use a Twilio virual number
VERIFIED_NUMBER = os.environ["phone number verified with Twilio"]

# Optionally, use os.environ[] if you don't want to change code every time you want to change company
STOCK_NAME = "INTC"
COMPANY_NAME = "Intel Corporation"    # Let's say you want to watch investments in Intel after CHIPS Act

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ["ALPHAVANTAGE API KEY"]
NEWS_API_KEY = os.environ["NEWSAPI API KEY"]
TWILIO_SID = os.environ["TWILIO ACCOUNT SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO AUTH TOKEN"]

# When stock price increase or decreases by 5% between yesterday and the day before yesterday

# Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
# print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
# print(day_before_yesterday_closing_price)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

up_down = None

if difference > 0:
    up_down = "UP ⬆"
else:
    up_down = "DOWN ⬇"

# Work out the percentage difference in price between closing price yesterday 
# and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
# print(diff_percent)

# Use the News API to get articles related to the COMPANY_NAME
# If difference percentage is greater than 5 then send messages
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Create a list that contains the first 4 articles.
    four_articles = articles[:4]
    # print(four_articles)

    # Use Twilio to send a separate message with each article's title and description to your phone number

    # Create a new list of the first 4 articles with headline and description using list comprehension
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in four_articles]
    # print(formatted_articles)

    # Send each article as a separate message via Twilio.    
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
