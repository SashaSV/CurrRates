import json

from dbCurrancy import db, appDb, Currancy, fillTableCurr
from rates import  get_external_rate, get_external_history_rate
from extApi import get_rate_hystory
from datetime import datetime

if __name__ == '__main__':
    with appDb.app_context():
        db.create_all()
        fillTableCurr()

        #get_external_rate()
        #get_external_history_rate(30)
        rates = get_rate_hystory('AUD', datetime.strptime('2023-01-10', '%Y-%m-%d').date())
        #j = json.dumps(rates)
        print(rates)




