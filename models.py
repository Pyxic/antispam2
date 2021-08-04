import re
import string

from peewee import *
from settings import db
from utils import is_digit


class BaseModel(Model):
    class Meta:
        database = db


class Chat(BaseModel):
    id = PrimaryKeyField(null=False)
    chat_id = CharField(max_length=100)
    message_id = IntegerField()
    username = CharField(max_length=100)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    text = TextField()

    # @staticmethod
    # def add_message(chat_id):
    #     if Chat.filter(chat_id=chat_id):
    #         return "Этот чат уже добавлен"
    #     if is_digit(chat_id):
    #         Chat.create(chat_id=chat_id)
    #         return "Чат успешно добавлен"
    #     else:
    #         return "Неверный идентификатор"


class Keywords(BaseModel):
    id = PrimaryKeyField(null=False)
    word = CharField(max_length=50)

    @staticmethod
    def has_keyword(message: str):
        keywords = [row.word for row in Keywords.select(Keywords.word)]
        message = message.lower()
        translator = re.compile('[%s]' % re.escape(string.punctuation))
        translator.sub(' ', message)
        message = re.sub(' +', ' ', message).strip()
        message = message.split()
        for keyword in keywords:
            if keyword in message:
                print(keyword)
                return True
        return False


if __name__ == '__main__':
    try:
        db.connect()
        Chat.create_table()
        Keywords.create_table()
        db.close()
    except InternalError as px:
        print(str(px))
