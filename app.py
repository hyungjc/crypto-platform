from os import access
from flask import render_template
from flask import request
import requests
from flask import Flask, redirect, url_for, request
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from operator import itemgetter
import json
import itertools

app = Flask(__name__)

var = None


def convert_time(unix):
    datetime_obj = datetime.fromtimestamp(unix/1000)  # in ms
    return datetime_obj.strftime("%Y.%m.%d")


class Korbit:
    def __init__(self, secret_key, public_key, access_token):
        self.secret_token = secret_key
        self.public_key = public_key
        self.access_token = access_token

    def __repr__(self):
        return f"{self.secret_token}, {self.public_key}, {self.access_token}"

    # @app.route('/transfers')
    def get_transfer(self):

        url = "https://api.korbit.co.kr/v1/user/transfers"

        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Bearer {}".format(self.access_token)
        print(headers)

        resp = requests.get(url, headers=headers)

        print(resp.status_code)

        obj = resp.json()
        # print(obj["amount"])
        print(obj)
        dict = {'deposit': [], 'withdraw': []}
        for i in obj:
            if i['type'] == 'deposit':
                dict['deposit'].append(
                    (convert_time(i['completed_at']), i['amount']))
            elif i['type'] == 'withdraw':
                dict['withdraw'].append(
                    (convert_time(i['completed_at']), i['amount']))

        print(dict)
        return dict


@ app.route('/login', methods=['POST'])
def login():
    pvt = request.form['api_secret']
    pub = request.form['api_public']

    url = "https://api.korbit.co.kr/v1/oauth2/access_token"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = "client_id={}&client_secret={}&grant_type=client_credentials".format(
        pub, pvt)
    resp = requests.post(url, headers=headers, data=data)
    # print(resp.status_code)
    obj = resp.json()
    global var
    var = Korbit(pvt, pub, obj["access_token"])

    return repr(var)


@ app.route('/transfers', methods=['POST'])
def print_transfers():
    pvt = request.form['api_secret']
    pub = request.form['api_public']

    url = "https://api.korbit.co.kr/v1/oauth2/access_token"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = "client_id={}&client_secret={}&grant_type=client_credentials".format(
        pub, pvt)
    resp = requests.post(url, headers=headers, data=data)
    # print(resp.status_code)
    obj = resp.json()
    global var
    var = Korbit(pvt, pub, obj["access_token"])

    return var.get_transfer()


@ app.route('/volume')
def print_volume():
    url = "https://api.korbit.co.kr/v1/ticker/detailed/all"

    resp = requests.get(url)

    obj = resp.json()
    # print(obj)

    total_vol = 0.0

    for i in obj:
        total_vol += float(obj[i]['volume'])

    #obj = sorted(obj.items(), key=lambda x: x[1]['volume'], reverse=True)

    # print(obj)

    dict_vol = {}  # still need to fix sorting doesnt work

    for key in obj:
        dict_vol[key] = obj[key]['volume']

    print(dict_vol)

    sorted_vol = dict(
        sorted(dict_vol.items(), key=lambda item: item[1], reverse=True))

    print(sorted_vol)

    sorted_top_five = {}

    sorted_top_five = dict(itertools.islice(sorted_vol.items(), 10))
    print()

    return json.dumps(sorted_vol)


@ app.route('/')
def index():
    return render_template('login.html')


if __name__ == "__main__":

    app.run(debug=True)


# Checklist

# timer for 60mins because accesstoken is valid for 60mins.
# able to refresh it and if time passes, need to login again using api secret and public keys
# have charts for assets, for top 5 trading volume, order change of price,
# do i need a db? <- thing to consider
