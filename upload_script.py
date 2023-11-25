import json

import connect
from models import Author, Quote

NAME_DATA = 'authors_and_quotes'

with open('authors.json', 'r', encoding='utf-8') as authors_file:
    authors_data = json.load(authors_file)

for author_info in authors_data:
    author_name = author_info['fullname']
    existing_author = Author.objects(fullname=author_name).first()

    if not existing_author:
        author = Author(
            fullname=author_info['fullname'],
            born_date=author_info['born_date'],
            born_location=author_info['born_location'],
            description=author_info['description']
        )
        author.save()
    else:
        print(f"Author '{author_name}' already exists.")

with open('quotes.json', 'r', encoding='utf-8') as quotes_file:
    quotes_data = json.load(quotes_file)

for quote_info in quotes_data:
    author_name = quote_info['author']
    author = Author.objects(fullname=author_name).first()

    if author:
        existing_quote = Quote.objects(author=author, quote=quote_info['quote']).first()
        if not existing_quote:
            quote_text = quote_info['quote']
            existing_quote = Quote.objects(author=author, quote=quote_text).first()

            if not existing_quote:
                quote = Quote(
                    tags=quote_info['tags'],
                    author=author,
                    quote=quote_text
                )
                quote.save()
            else:
                print(f"Quote '{quote_text}' by '{author_name}' already exists.")
        else:
            print(f"Quote '{quote_info['quote']}' by '{author_name}' already exists.")
    else:
        print(f"Author '{author_name}' not found.")
