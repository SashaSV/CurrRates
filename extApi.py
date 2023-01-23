from dbCurrancy import db, appDb, Currancy, Currancy_rates
from flask import Flask, request, jsonify
from datetime import datetime
from rates import  get_external_rate

app = Flask(__name__)

@app.route('/api/currency/history')
def get_rate_hystory_rest():
    c_code = request.args.get('code')
    d_from = request.args.get('date_from')

    with appDb.app_context():
        db.create_all()
        date_f = datetime.strptime(d_from, '%Y-%m-%d').date()
        ratesDb = get_rate_hystory(c_code, date_f)

    return jsonify(ratesDb)

def get_rate_hystory(currancy_code=None, date_from=None):

    cur_id = Currancy.query.filter(Currancy.code == currancy_code).first()
    rates = []

    if not Currancy_rates.query.filter(Currancy_rates.date == datetime.today().date()).first():
        get_external_rate()

    if cur_id:
        ratesDb = Currancy_rates.query. \
            filter(  True if currancy_code == None else Currancy_rates.id_curr == cur_id.id). \
            filter( True if date_from == None else Currancy_rates.date >= date_from).\
            order_by(Currancy_rates.id_curr, Currancy_rates.date).all()

        for rate in ratesDb:
            ds = datetime(rate.date.year, rate.date.month, rate.date.day, 0, 0).strftime('%Y-%m-%d')
            rates.append(
                {
                    'Date': ds ,
                    'Code': Currancy.query.get(rate.id_curr).code,
                    'Rate': str(rate.rate),
                }
            )
    else:
        if currancy_code:
            rate = get_external_rate(currancy_code)
            if rate >0:
                rates.append(
                    {
                        'Date': datetime.now().strftime('%Y-%m-%d'),
                        'Code': currancy_code,
                        'Rate': str(rate),
                    }
            )
    return rates

if __name__ == '__main__':
    app.run()