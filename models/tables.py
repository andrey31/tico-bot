from os import environ

from peewee import (MySQLDatabase, Model, CharField,
                    IntegerField, ForeignKeyField, DateTimeField)


PASS_DB = environ['PASS_DB_TICOBOT']

# Connect to a MySQL database on network.
db = MySQLDatabase('ticobot', user='ticobot', password=PASS_DB,
                   host='db', port=3306, charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        table_name = 'users'

    id_user = IntegerField()
    username = CharField()
    first_name = CharField()
    last_name = CharField()


class Message(BaseModel):
    class Meta:
        table_name = 'messages'
    user = ForeignKeyField(User, backref='messages')
    date = DateTimeField()


def create_tables():
    with db:
        db.create_tables([User, Message])
