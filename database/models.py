from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('history.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    name = pw.CharField()
    telegram_id = pw.IntegerField()


class Query(BaseModel):
    user = pw.ForeignKeyField(User, backref='queries')
    body = pw.TextField()
    created_at = pw.DateField(default=datetime.now())
