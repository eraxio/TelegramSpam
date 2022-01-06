import requests
from bs4 import BeautifulSoup


def iter_free_proxy():
    html = requests.get('http://foxtools.ru/Proxy').content
    soup = BeautifulSoup(html, 'lxml')
    line = soup.find('table', id='theProxyList').find('tbody').find_all('tr')
    for tr in line:
        td = tr.find_all('td')
        ip = td[1].text
        port = td[2].text
        # country = td[3].text.replace('\xa0', '')
        # anonym = td[4].text.replace('\r\n        ', '')
        # types = td[5].text.replace('\r\n\t\t\t\t\t', '') \
        # .replace('\r\n        ', '')
        # time = td[6].text

        proxy = {
            "ip": ip,
            "port": port,
            "login": None,
            "password": None
        }

        yield proxy


def get_free_proxy():
    return [proxy for proxy in iter_free_proxy()]
