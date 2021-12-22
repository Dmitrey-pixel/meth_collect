
# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге
# MongoDB и реализовать функцию, которая будет добавлять
# только новые вакансии/продукты в вашу базу.
# 2. Написать функцию, которая производит поиск и выводит на экран
# вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['vac_hh']
data_scientist = db.data_scientist

main_url = 'https://hh.ru'

search_vacancy = 'data scientist'
page = 0
params = {'area': '1',
          'professional_role': '96',
          'text': search_vacancy,
          'page': page}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)

while True:
    if response.ok:
        dom = bs(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

        for vacancy in vacancies:
            vacancy_data = {}
            info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            name = info.text
            link = info.get('href')

            if vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}) is not None:
                employer = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            else:
                employer = None

            wage_info = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

            if wage_info is not None:
                wage_interval = wage_info.text.split()

                if wage_interval[0] == 'от':
                    min_wage = int(wage_interval[1] + wage_interval[2])
                    currency = wage_interval[3]
                    max_wage = None
                elif wage_interval[0] == 'до':
                    max_wage = int(wage_interval[1] + wage_interval[2])
                    currency = wage_interval[3]
                    min_wage = None
                else:
                    min_wage = int(wage_interval[0] + wage_interval[1])
                    max_wage = int(wage_interval[3] + wage_interval[4])
                    currency = wage_interval[5]
            else:
                max_wage = None
                min_wage = None
                currency = None

            vacancy_data['_id'] = link.split('?')[0].split('/')[-1]
            vacancy_data['vacancy'] = name
            vacancy_data['max_wage'] = max_wage
            vacancy_data['min_wage'] = min_wage
            vacancy_data['currency'] = currency
            vacancy_data['link'] = link
            vacancy_data['employer'] = employer
            vacancy_data['source'] = main_url

            try:
                data_scientist.insert_one(vacancy_data)
            except dke:
                pass

        if dom.find('a', {'data-qa': 'pager-next'}) is not None:
            next_url = dom.find('a', {'data-qa': 'pager-next'}).get('href')
            response = requests.get(main_url + next_url, headers=headers)

        else:
            break

print(f'Всего вакансий: ', data_scientist.count_documents({}))
# for doc in data_scientist.find({}):
#     pprint(doc)

def wage_searcher():
    basic_wage = int(input('Введите желаемую зарплату: '))
    vacancy_list = []
    for doc in data_scientist.find({'$or':
                                       [{'min_wage': {'$gt': basic_wage}},
                                        {'max_wage': {'$gt': basic_wage}}
                                         ]}):
        vacancy_list.append(doc)

    print(f'Количество подходящих вакансий: {len(vacancy_list)}')
    return vacancy_list

pprint(wage_searcher())

