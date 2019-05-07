from peewee import *
import config


dbhandle = MySQLDatabase(
    config.database_name,
    host=config.server_IP,
    user=config.user_name,
    password=config.user_password,
)


class BaseModel(Model):
    class Meta:
        database = dbhandle


class User(BaseModel):

    whois = CharField()
    date = CharField()
    time = CharField()
    number = CharField()
    how_long = CharField()


class Names(BaseModel):
    whois = CharField(unique=True)
    name = CharField()