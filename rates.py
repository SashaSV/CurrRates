import requests
from dbCurrancy import db, Currancy, Currancy_rates
from datetime import datetime
from datetime import timedelta
import json
import os

__api_key = "688a4ecad5e7d69ddf9f08b1"

# определить курс валют по внешней API
# Курсы для валют, которые сохранены в таблице Currancy, сохраняются
# в таблице Currancy_rates
# Т.к. кол-во бесплатных обращений к API ограничено, применяется кеш в предлах суток
def get_external_rate(code = None):

    # сформировать название файла с кешом
    cache_filename = get_filename_for_cache(date=datetime.now())

    # проверить кеш с курсом на дату
    conversion_rates = get_file_from_cache(cache_filename)

    if len(conversion_rates) == 0:
        url = 'https://v6.exchangerate-api.com/v6/{0}/latest/USD'.format(__api_key)
        conversion_rates = get_rates_from_external_api( url, cache_filename)

    rates = conversion_rates.get('conversion_rates')

    date = datetime.fromtimestamp(conversion_rates['time_last_update_unix'])
    currances = Currancy.query.all()
    for curr in currances:
        if rates.__contains__(curr.code):
            rate = Currancy_rates.query.\
                filter(Currancy_rates.id_curr == curr.id).\
                filter(Currancy_rates.date == date.date()).first()
            if not rate:
                rate = Currancy_rates(curr.id, rates.get(curr.code), date)
                db.session.add(rate)
                db.session.commit()
            else:
                rate.rate = rates.get(curr.code)
                db.session.commit()

            print('{0}={1}, {2}'.format(curr.code,rates.get(curr.code), date))

    ret_rate = -1
    if code:
        if rates.__contains__(code):
            ret_rate = rates.get(code)
    return ret_rate

def get_external_history_rate(days):
    import requests
    day_start = datetime.now().today() - timedelta(days=days)
    day_finish = datetime.now().today()-timedelta(days=1)

    cache_filename = get_filename_for_cache_ft(date_from=day_start,date_to=day_finish)

    # open cache from file
    conversion_rates = get_file_from_cache(cache_filename)

    if len(conversion_rates) == 0:
        url = "https://api.apilayer.com/fixer/timeseries?start_date={0}&end_date={1}&base=USD&symbols=UAH,RUR,RUB,PLN,EUR,CAD"\
            .format(
            day_start.date(), day_finish.date())

        payload = {}
        headers = {
            "apikey": "u7QHuc8Pf6n5niDOLwLdoaVB9bcJlpvp"
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.text
        conversion_rates = json.loads(result)

        dump_to_json(cache_filename, conversion_rates)

    rates = conversion_rates.get('rates')

    currances = Currancy.query.all()

    for date_str, rates in rates.items():
        for curr in currances:
            if rates.__contains__(curr.code):

                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                print(date, curr.code, rates[curr.code])
                rate = Currancy_rates.query. \
                    filter(Currancy_rates.id_curr == curr.id). \
                    filter(Currancy_rates.date == date).first()
                if not rate:
                    rate = Currancy_rates(curr.id, rates.get(curr.code), date)
                    db.session.add(rate)
                    db.session.commit()
                else:
                    rate.rate = rates.get(curr.code)
                    db.session.commit()

# Сохранение JSON <data> в файл <filename>
def dump_to_json(filename, data, **kwargs):
    kwargs.setdefault('ensure_ascii', False)
    kwargs.setdefault('indent', 1)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, **kwargs)

def get_file_from_cache(cache_filename):
    conversion_rates = []
    if os.path.exists(cache_filename):
        with open(cache_filename, encoding='utf-8') as json_file:
            conversion_rates = json.load(json_file)
    return conversion_rates

def get_filename_for_cache(date):
    return '{0}\\cache\\{1}.json'.format(os.getcwd(), date.date())

def get_filename_for_cache_ft(date_from, date_to):
    return '{0}\\cache\\{1}_{2}.json'.format(os.getcwd(), date_from.date(), date_to.date())

def get_rates_from_external_api(url, cache_filename):

    # Making our request
    response = requests.get(url)

    # JSON object
    conversion_rates = response.json()

    # save cache into file
    dump_to_json(cache_filename, conversion_rates)

    return conversion_rates