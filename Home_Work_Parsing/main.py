import requests
from bs4 import BeautifulSoup
import re
import json

URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
regular = r'((d|D)jango)|((F|f)lask)'


def http_get(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    response = requests.get(
        url,
        headers=headers
    )
    return response


def parse_vacancys(response):
    parsed = []
    soup = BeautifulSoup(response.text, features='lxml')
    vacancys = soup.find_all('div', attrs={'class': 'serp-item'})
    for vacancy in vacancys:
        a = vacancy.find('a')
        url = a.attrs['href']
        demands = parse_content(http_get(url))
        if re.search(regular, ','.join(demands)):
            fee = vacancy.find(
                'span',
                attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            fee = ' '.join(re.split(r'\u202f', fee))
            company = vacancy.find(
                'a',
                attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            company = ' '.join(re.split(r'\s', company))
            city = vacancy.find(
                'div',
                attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            city = city.split(',')[0]
            dict_vacancy = {'url': url, 'fee': fee, 'company': company, 'city': city}
            parsed.append(dict_vacancy)
    print(parsed)
    return parsed


def parse_content(response):
    demands = []
    soup = BeautifulSoup(response.text, features='lxml')
    section = soup.find_all('span', attrs={'data-qa': "bloko-tag__text"})
    for demand in section:
        demands.append(demand.text)
    return demands


if __name__ == '__main__':
    vacancys = parse_vacancys(http_get(URL))
    with open('vacancys.json', 'w', encoding='utf-8') as file:
        json.dump(vacancys, file, indent=3, ensure_ascii=False)
