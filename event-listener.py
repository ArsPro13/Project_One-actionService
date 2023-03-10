import requests
import time
from bs4 import BeautifulSoup

prev_price = 0
while True:
    url_to_crawl = "https://www.onlinetrade.ru/catalogue/pylesosy-c521/tefal/pylesos_tefal_compact_power_xxl_tw4825ea_s_konteynerom-3060763.html"
    response = requests.get(url_to_crawl)
    text = response.text

    pos = text.find('itemprop="price"')
    text = text[pos:]
    pos = text.find('">') + 2
    text = text[pos:]
    pos = text.find('</span>')
    text = text[:pos]
    text = text.replace(" ", "").strip()
    new_price = int(text)
    
    if (new_price != prev_price):
      print("Price has changed")
      print("Old price:", prev_price)
      print("New price:", new_price)
      print("Difference:", new_price - prev_price)
      prev_price = new_price
    else:
      print("The price has not changed")
    time.sleep(10)