import requests
import json
from bs4 import BeautifulSoup

# Функція для отримання даних про цитати та авторів
def scrape_quotes_and_authors():
    all_quotes = []
    all_authors = []
    added_authors = set()

    base_url = 'http://quotes.toscrape.com'
    current_page = '/page/1'

    while current_page:
        response = requests.get(base_url + current_page)
        soup = BeautifulSoup(response.content, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]

            all_quotes.append({
                'tags': tags,
                'author': author,
                'quote': text
            })

            # Отримання додаткової інформації про авторів
            author_info_link = base_url + quote.find_next('a')['href']
            author_info_response = requests.get(author_info_link)
            author_soup = BeautifulSoup(author_info_response.content, 'html.parser')

            fullname = author_soup.find('h3', class_='author-title').text.strip()
            born_date_element = author_soup.find('span', class_='author-born-date')
            born_location_element = author_soup.find('span', class_='author-born-location')

            born_date = born_date_element.text.strip() if born_date_element else ''
            born_location = born_location_element.text.strip() if born_location_element else ''

            description = author_soup.find('div', class_='author-description').text.strip()
            if fullname not in added_authors:
                author_data = {
                    'fullname': fullname,
                    'born_date': born_date,
                    'born_location': born_location,
                    'description': description
                }
                all_authors.append(author_data)
                added_authors.add(fullname)

        next_page = soup.find('li', class_='next')
        current_page = next_page.find('a')['href'] if next_page else None

    # Запис у quotes.json
    with open('quotes.json', 'w', encoding='utf-8') as file:
        json.dump(all_quotes, file, ensure_ascii=False, indent=2)

    # Запис у authors.json
    with open('authors.json', 'w', encoding='utf-8') as file:
        json.dump(all_authors, file, ensure_ascii=False, indent=2)

# Виклик функції для скрапінгу
scrape_quotes_and_authors()
