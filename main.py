import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from requests_html import HTMLSession
import json
import re

def gen_headers():
    headers = Headers(browser='chrome', os='win')
    return headers.generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=gen_headers())
print(response.status_code)

html_data = response.text
soup = BeautifulSoup(html_data, 'lxml')
vacancy_list = soup.find_all('div', id='a11y-main-content')
vacancies = []
for vacancy in vacancy_list:
    a_tag = vacancy.find('a', class_='bloko-link')
    company_tag = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary')
    city_tag = vacancy.find('div', class_='vacancy-serp-item-company')
    salary_tag = vacancy.find('span', class_='bloko-header-section-2')

    link = a_tag['href']
    company = company_tag.text.strip()
    city = city_tag.text.strip()
    salary = salary_tag.text
    if salary is not None:
        pattern = re.compile(r'\u202f')
        repl = ' '
        salary = re.sub(pattern, repl, salary)
    if salary is None:
        salary = 'Не указана'

    session = HTMLSession()
    response = session.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    vacancy_tag = soup.find('div', class_='g-user-content')
    vacancy_text = vacancy_tag.text
    searchwords_1 = 'Flask'
    searchwords_2 = 'Django'
    if searchwords_1.lower() or searchwords_2.lower() in vacancy_text.lower():
        result = {
            'ссылка': link,
            'компания': company,
            'город': city,
            'зарплата': salary
        }
        vacancies.append(result)

with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(vacancies, file, ensure_ascii=False, indent=4)

print(vacancies)

