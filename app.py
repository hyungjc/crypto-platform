
from os import access
from flask import render_template
from flask import request
import requests
from flask import Flask, redirect, url_for, request
from requests.structures import CaseInsensitiveDict
app = Flask(__name__)


class Korbit:
    def __init__(self, secret_key, public_key, access_token):
        self.secret_token = secret_key
        self.public_key = public_key
        self.access_token = access_token

    def __repr__(self):
        return f"{self.secret_token}, {self.public_key}, {self.access_token}"


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
    x = Korbit(pvt, pub, obj["access_token"])
    return repr(x)

    r = requests.get()


def get_transaction()


@app.route('/')
def index():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
