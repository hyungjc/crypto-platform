

from os import access
from flask import render_template
from flask import request
import requests
from flask import Flask, redirect, url_for, request
from requests.structures import CaseInsensitiveDict
app = Flask(__name__)

var = None


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
                dict['deposit'].append(i['amount'])
            elif i['type'] == 'withdraw':
                dict['withdraw'].append(i['amount'])

        print(dict)
        return dict


@app.route('/login', methods=['POST'])
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


@app.route('/transfers', methods=['POST'])
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


@app.route('/volume', methods=['POST'])
def print_volume():
    return 'hi'


@app.route('/')
def index():
    return render_template('login.html')


if __name__ == "__main__":

    app.run(debug=True)


# Checklist

# timer for 60mins because accesstoken is valid for 60mins.
# able to refresh it and if time passes, need to login again using api secret and public keys
# have charts for assets, for top 5 trading volume, order change of price,
