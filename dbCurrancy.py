from flask import Flask
from flask_sqlalchemy import SQLAlchemy

appDb = Flask(__name__)
appDb.secret_key = 'hello'
appDb.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:111111@localhost:5432/convertor_test"

db = SQLAlchemy(appDb)
db.init_app(appDb)

# Таблица с валютами, по которым необходимо хранить курсы
class Currancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True)
    name = db.Column(db.String(100))
    country = db.Column(db.String(50))
    number = db.Column(db.Integer)

    def __init__(self, code, name, country, number):
        self.code = code
        self.name = name
        self.country = country
        self.number = number

    def __repr__(self):
        return '%r' % self.code

# Таблица с курсами валют на дату
# relationship на Currancy не настраивал, хотя нужно было бы
class Currancy_rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_curr = db.Column(db.Integer) # код курса валют по Currancy
    rate = db.Column(db.DECIMAL(15,4)) # курс валют
    date = db.Column(db.Date) # дата курса валют

    def __init__(self, id_curr, rate, date):
        self.id_curr = id_curr
        self.rate = rate
        self.date = date

    def __repr__(self):
        return 'Date {0}, Rate {1}, {2}'.format(self.date, str(self.rate), self.id_curr)

# наполнение таблицы Currancy валютами из задания
def fillTableCurr():

    if not Currancy.query.filter(Currancy.code == 'UAH').first():
        cur = Currancy('UAH', 'Hryvnia', 'UKRAINE', 980)
        db.session.add(cur)
    if not Currancy.query.filter(Currancy.code == 'RUR').first():
        cur = Currancy('RUR', 'Russian Ruble (befor 1998)', 'RUSSIAN FEDERATION (THE)', 810)
        db.session.add(cur)
    if not Currancy.query.filter(Currancy.code == 'RUB').first():
        cur = Currancy('RUB', 'Russian Ruble', 'RUSSIAN FEDERATION (THE)', 643)
        db.session.add(cur)
    if not Currancy.query.filter(Currancy.code == 'PLN').first():
        cur = Currancy('PLN', 'Zloty', 'POLAND', 985)
        db.session.add(cur)
    if not Currancy.query.filter(Currancy.code == 'EUR').first():
        cur = Currancy('EUR', 'Euro', 'EUROPEAN UNION', 978)
        db.session.add(cur)
    if not Currancy.query.filter(Currancy.code == 'CAD').first():
        cur = Currancy('CAD', 'Canadian Dollar', 'CANADA', 124)
        db.session.add(cur)
    db.session.commit()

