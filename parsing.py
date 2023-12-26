from bs4 import BeautifulSoup
import requests

def parsing_akipress():
    url = 'https://akipress.org/'
    response = requests.get(url=url)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    all_news = soup.find_all('a', class_='newslink')
    # print(all_news)
    n = 0
    for news in all_news:
        n += 1
        print(n, news.text)
        with open('news.txt', 'a+', encoding='utf-8') as news_file:
            news_file.write(f'{n}) {news.text}\n')

def parsing_sulpak():
    n = 0
    for page in range(1, 6):
        url = f'https://www.sulpak.kg/f/noutbuki?page={page}'
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')
        all_laptops = soup.find_all('div', class_='product__item-name')
        # print(all_laptops)
        for laptop in all_laptops:
            n += 1
            print(n, laptop.text)
parsing_sulpak()
