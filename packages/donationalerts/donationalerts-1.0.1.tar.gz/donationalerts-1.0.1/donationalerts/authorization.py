#Donation Alerts v1.0.0
#by @cxldxice

import logging
import os
import sys
import webbrowser

import flask
import requests
from flask import Flask, redirect, request

app = Flask(__name__) #server
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Authorization(object):
    def __init__(self, client_id, client_secert):
        global client
        global secret

        client = client_id
        secret = client_secert


    @staticmethod
    @app.route("/")
    def __index__():
        return redirect(f"https://www.donationalerts.com/oauth/authorize?client_id={client}&redirect_uri=http://127.0.0.1:5000/auth&response_type=code&scope=oauth-donation-index")

    @staticmethod
    @app.route("/auth")
    def __auth__():
        code = request.args.get("code")

        data = {
            "client_id": client,
            "client_secret": secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:5000/auth",
            "scope": "oauth-donation-index"
        }

        out = requests.post("https://www.donationalerts.com/oauth/token", data=data).json()

        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")

        try:
            token = out["access_token"]
            print("Token > "+token)

            return redirect(f"/success/{token}")
        except:
            print("Error > "+str(out))
            return redirect(f"/error?error_data={out}")
        
    @staticmethod
    @app.route("/success/<token>")
    def __success__(token):
        return flask.render_template("auth.html", token=token)

    @staticmethod
    @app.route("/error")
    def __error__():
        error = request.args.get("error_data")

        return flask.jsonify(error)


    def start_authorization(self):
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")
        
        print("Warning!!!\nredirect_uri must be http://127.0.0.1:5000/auth\nchange on https://www.donationalerts.com/application/clients\n\npress ENTER to start")

        input()

        webbrowser.open("http://127.0.0.1:5000")
        app.run(port=5000)
