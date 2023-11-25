from mongoengine import Document
from mongoengine.fields import StringField, ReferenceField, ListField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

    meta = {'collection': 'authors_collection'}


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

    meta = {'collection': 'quotes_collection'}
