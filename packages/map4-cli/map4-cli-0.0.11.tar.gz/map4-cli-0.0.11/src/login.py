import webbrowser
from flask import Flask, request, Response, redirect
import logging
import requests
from typing import NamedTuple
import json
import threading
from werkzeug.serving import make_server
import time
import boto3
from .docker_process import Docker

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
idp_client = boto3.client(
                'cognito-idp'
            )
id_client = boto3.client('cognito-identity')
client_id = "2ca2uqrv1p0uvfca4itd51mng4"
user_pool_id = "ap-northeast-1_1wAcm9FiA"

class Token(NamedTuple):
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class Credential(NamedTuple):
    access_key_id: str
    secret_key: str
    session_token: str

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 1234, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        log.info('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


class EndpointAction(object):
    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response

class Login:
    def __init__(self):
        self.server = None

    def run_server(self):
        app.add_url_rule("/auth/code", "auth_handler", self.auth_code_handler)
        app.add_url_rule("/success", "login_success_handler", self.login_success_handler)

        #app.run(debug=False, port=1234)
        self.server = ServerThread(app)
        self.server.start()

    def move_to_login_page(self):
        url = "https://map4clitest.auth.ap-northeast-1.amazoncognito.com/login?response_type=code&client_id=2ca2uqrv1p0uvfca4itd51mng4&redirect_uri=http://localhost:1234/auth/code&state=STATE&scope=openid+aws.cognito.signin.user.admin"
        webbrowser.open(url)
        self.run_server()

    def sleep_shutdown(self):
        time.sleep(0.5)
        self.server.shutdown()
        print("\nProject created! you can run by below command.")
        print("\ncd map4_engine_ui\nmap4cli run\n")

    def login_success_handler(self):
        threading.Thread(target=self.sleep_shutdown).start()
        name = "Login completed! Please close this page."
        return name

    def auth_code_handler(self):
        try:
            code = request.args.get("code")
            token = self.get_token(code)
            identityid = self.get_id(token.id_token)
            credential = self.get_credentials_for_identity(identityid, token.id_token)
            print("Login Succeeded!")
            print("Pull Images...")
            d = Docker()
            d.pull(credential)
            return redirect("/success")
        except Exception as err:
            print(err)
            return err

    def get_token(self, code: str):
        endpoint = "https://map4clitest.auth.ap-northeast-1.amazoncognito.com/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {"grant_type": "authorization_code", "client_id": "2ca2uqrv1p0uvfca4itd51mng4", "redirect_uri": "http://localhost:1234/auth/code", "code": code}
        res = requests.post(endpoint, headers=headers, params=payload)
        if res.status_code == 400:
            raise Exception(res.text)
        json_token = res.json()
        token = Token(
            json_token["access_token"], 
            json_token["id_token"], 
            json_token["refresh_token"], 
            json_token["token_type"], 
            json_token["expires_in"], 
        )
        return token

    def store_token(self, token: Token):
        with open('./test.json', 'w') as f:
            json.dump(token._asdict(), f, indent=4)

    def get_id(self, idtoken):
        response = id_client.get_id(
            AccountId='307148723122',
            IdentityPoolId="ap-northeast-1:2c6968a9-05b7-4309-89e5-fa31783d8412",
            Logins={
                #"logins_key": idtoken,
                'cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_1wAcm9FiA': idtoken
            }
        )
        return response["IdentityId"]

    def get_credentials_for_identity(self, identityid, idtoken):
        response = id_client.get_credentials_for_identity(
            IdentityId=identityid,
            Logins={
                'cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_1wAcm9FiA': idtoken
            }
        )
        credential = Credential(
            response["Credentials"]["AccessKeyId"],
            response["Credentials"]["SecretKey"],
            response["Credentials"]["SessionToken"]
        )
        return credential

    def admin_initiate_auth(self, username, password):
        response = idp_client.initiate_auth(
                    ClientId=client_id,
                    AuthFlow="USER_PASSWORD_AUTH",
                    AuthParameters={
                        "USERNAME": username,
                        "PASSWORD": password,
                    }
                )
        return response
    