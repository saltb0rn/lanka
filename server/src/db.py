#!/usr/bin/python3

import os
import peewee

DATABASE = os.environ.get('DATEBASE')

if DATABASE == 'MYSQL':
    database = peewee.MySQLDatabase(
        database="USERDB",
        host=os.environ.get('MYSQL_HOST', '172.25.0.2'),
        user="saltborn",
        password="saltborn",
        charset="utf8mb4")
else:
    database = peewee.SqliteDatabase(os.path.join(
        os.path.dirname(__file__), 'userdb.db'))


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    email = peewee.CharField()
    join_date = peewee.DateTimeField(formats="%y/%m/%d %H:%M:%S")


class LoginRecord(BaseModel):
    sno = peewee.AutoField()
    username = peewee.CharField()
    login_date = peewee.DateTimeField(formats="%y/%m/%d %H:%M:%S")
    credential = peewee.CharField()
    valid = peewee.BooleanField(default=True)


class Message(BaseModel):
    sno = peewee.AutoField()
    username = peewee.CharField()
    date = peewee.DateTimeField(formats="%y/%m/%d %H:%M:%S")
    message = peewee.TextField()


def create_tables():
    with database:
        database.create_tables([User, LoginRecord, Message])
        # migrator = playhouse.migrate.MySQLMigrator(database)

        # login_record_credential_field = peewee.CharField(default="")
        # login_record_valid_field = peewee.BooleanField(default=True)

        # playhouse.migrate.migrate(
        #     migrator.add_column('loginrecord', 'credential',
        #                         login_record_credential_field),
        #     migrator.add_column('loginrecord', 'valid',
        #                         login_record_valid_field))
