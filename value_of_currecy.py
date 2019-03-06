from bs4 import BeautifulSoup
import requests
import sys

def exchange_rates(currency, format = 'full'):
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()['Valute']
    if currency in response:
        data = response[currency]
    else:
        return 'Unknown currecy!'
    if format == 'full':
        return data
    elif format == 'value':
        return data['Value']
    else:
        return 'Unknown format!'

var = sys.argv[1]
if var:
    ans = exchange_rates(var, 'value')
else:
    ans = exchange_rates('EUR', 'value')
print(ans)