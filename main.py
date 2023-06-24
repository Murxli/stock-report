import requests
from datetime import datetime
from twilio.rest import Client

today = str(datetime.now().date())

time_frame = "TIME_SERIES_DAILY"
stock_symbol = "TSL"
stock_name = "tesla"

news_url = "https://newsapi.org/v2/everything"
stock_url = f"https://www.alphavantage.co/query"

alpha_vantage_api_key = "MIBVRFZTKYD6537G"
newsapi_key = "6073aed26ec24dd590e291e7c5ddab17"

twilio_account_sid = "AC1db8ff9313987a8cd30ca98b0d42edc4"
twilio_auth_token = "0fd86924f672b622be73d1ce4249d8d7"

stock_parameters = {
    "function" : time_frame,
    "symbol" : stock_symbol,
    "apikey" : alpha_vantage_api_key
}

news_parameters = {

    "apiKey" : newsapi_key,
    "qinTitle" : stock_name

}

def get_news() :
    news_response = requests.get(url= news_url, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    news_list = []
    for i in range(2) :
        news_title = news_data[i]["title"]
        news_description = news_data[i]["description"]
        news_tuple = (news_title, news_description)
        news_list.append(news_tuple)
    print(news_list)
    return news_list


def send_message(msg) :
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                body=msg,
                                to='whatsapp:+916379564694'
                            )

    print(message.sid)


stock_response = requests.get(url=stock_url, params=stock_parameters)
stock_response.raise_for_status()
data = stock_response.json()["Time Series (Daily)"]
last_traded_day = [i for i in data][0]

if today == last_traded_day :
    result = [(key,value) for (key,value) in data.items() ][:2]
    today_close = float(result[0][1]["4. close"])
    previous_close = float(result[1][1]["4. close"])
    print(previous_close, today_close)

    rate_change = round(((today_close-previous_close)/previous_close)*100, 2)
    
    print(rate_change)    

    if rate_change > 4.5 or rate_change< -4.5 :

        news_content = get_news()
        title1 = news_content[0][0]
        title2 = news_content[1][0]
        decription1 = news_content[0][1]
        decription2 = news_content[1][1]
            
        msg = f"""{stock_symbol} - {stock_name}\n
        Todays perfomace : {rate_change}\n\nNews related to {stock_name}:\n\n{title1.ljust(30)} :
        {decription1}\n\n{title2} :
        {decription2}\n
        Thats all for today's market"""
        print(msg)
        send_message(msg)

    else :
        msg = f"""{stock_symbol} - {stock_name}\n
        Todays perfomace : {rate_change}\n """
        send_message(msg)