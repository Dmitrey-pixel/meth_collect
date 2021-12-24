# 1. Написать приложение, которое собирает основные
# новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# 2. Сложить собранные новости в БД

from lxml import html
import requests
from pprint import pprint
from datetime import datetime

url = 'https://yandex.ru/news/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

yandex_news = dom.xpath("//div[contains(@class, 'news-top-flexible')]//div[contains(@class, 'mg-card ')]")

news_list = []

for item in yandex_news:
    news = {}
    text = item.xpath(".//h2[contains(@class, 'mg-card__title')]/a/text()")
    source = item.xpath(".//span[contains(@class, 'mg-card-source__source')]/a/text()")
    link = item.xpath(".//h2[contains(@class, 'mg-card__title')]/a/@href")
    data = item.xpath(".//span[contains(@class, 'mg-card-source__time')]/text()")

    news['title'] = text[0].replace('\xa0', ' ') if len(text) else None
    news['link'] = link[0] if len(link) else None
    news['source'] = source[0] if len(source) else None
    news['datetime'] = datetime.now().strftime("%Y-%m-%d") + ' ' + data[0] if len(data) else None

    news_list.append(news)

pprint(news_list)
