
# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH
# и/или Superjob. Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# 1. Наименование вакансии.
# 2. Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# 3. Ссылку на саму вакансию.
# 4. Сайт, откуда собрана вакансия.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


main_url = 'https://hh.ru'
page = 0
params = {'text': 'data scientist',
          'area': '1',
          'professional_role': '96',
          'page': page}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
vacancy_list = []
count = 1
while page < count:
    responce = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
    if responce.ok:
        dom = bs(responce.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': "vacancy-serp-item"})
        page += 1
        for vacancy in vacancies:
            vacancy_data = {}
            info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            name = info.text
            link = info.get('href')
            min_salary = None
            max_salary = None
            currency = None
            try:
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                st = salary.replace('\u202f', '').split()
                if st[0] == 'от':
                    min_salary = int(st[1])
                    max_salary = None
                elif st[0] == 'до':
                    min_salary = None
                    max_salary = int(st[1])
                else:
                    min_salary = int(st[0])
                    max_salary = int(st[2])
                currency = st[-1]
            except:
                min_price = None
                max_price = None
                currency = None

            vacancy_data['name'] = name
            vacancy_data['min_price'] = min_salary
            vacancy_data['max_price'] = max_salary
            vacancy_data['currency'] = currency
            vacancy_data['link'] = link
            vacancy_data['website'] = main_url

            vacancy_list.append(vacancy_data)

        num_page = dom.find_all('a', {'class', 'bloko-button'})
        count = int(num_page[-2].text)


pprint(vacancy_list)
