# stock_alerts

A simple python script that sends you articles based on the percentage the stock goes up and down. It uses 
a Twilio virtual number, and https://www.alphavantage.co/query and https://newsapi.org/v2/everything APIs,
but can be modified to use other APIs. It uses twilio.rest and requests libraries, and python's built in os
library.

Documentation:

twilio.rest:
https://www.twilio.com/docs/sms/quickstart/python

requests:
https://requests.readthedocs.io/en/latest/api/

NewsAPI:
https://newsapi.org/

Alpha Vantage:
https://www.alphavantage.co/

Don't know how to use environmental variables?
https://www.twilio.com/blog/environment-variables-python
https://www.twilio.com/blog/how-to-set-environment-variables.html

Don't have your own server to run/test this script contonuously? 
Try Anaconda's https://www.pythonanywhere.com/
Note: You'll need to set up new enironmental variables on server.