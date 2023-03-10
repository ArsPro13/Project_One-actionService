import requests
from bs4 import BeautifulSoup

url = 'https://market.yandex.ru/product--nabor-svechei-ikea-khedersam-v-stakane-svezhaia-trava-505-023-77/1777146441?cpc=E89znpfvyUGfEYn7vWwAGiooioK6y8rPtclnL1PudE4zYk_x5Se7vvbQRgH6Pm8kQGvKHYjyCu24zgUvdURADxc6F6d1-2ovE2UtmGpKgw82JzmGfXqoTw2Syib-YculrMVcSv0hOZifYnYVvKAw419XmQRFtPddw7biotLz2ni9JACYzYAowcZJcxJfTg45Hn38i6Db8pOEwAKFJ2MDE73z5oCtASuxs2dA4CBP6mW8eOTSgo6d6Q%2C%2C&sku=101853110140&offerid=v84_aw0vLTF3AEEqgbVcPg&cpa=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('title')

for quote in quotes:
    print(quote.text)
