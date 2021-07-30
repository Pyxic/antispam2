from environs import Env
from peewee import *
# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
admin_id = env.list('admin_id')
bot_id = env.int('bot_id')


user = env.str('SQL_USER', 'postgres')
password = env.str('SQL_PASSWORD', 'pass12345')
db_name = env.str('SQL_DATABASE', 'antispam')

db = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host=env.str('ALLOWED_HOSTS', 'localhost'),
    port=5432
)
