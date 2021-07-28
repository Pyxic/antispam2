from environs import Env
from peewee import *
# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
admin_id = env.list('admin_id')
bot_id = env.int('bot_id')


user = 'postgres'
password = 'pass12345'
db_name = 'antispam'

db = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)
