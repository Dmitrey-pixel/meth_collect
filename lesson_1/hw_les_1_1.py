
# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

username = input('Введите логин пользователя: ')

url = f"https://api.github.com/users/{username}/repos"
resp = requests.get(url)
j_data = resp.json()

repo = [f"{k} {i.get('name')}" for k, i in enumerate(j_data, 1)]
print(f"Список репозиториев пользователя {username}:", *repo, sep='\n')

with open("j_repo.json", "w") as f:
    json.dump(repo, f)
