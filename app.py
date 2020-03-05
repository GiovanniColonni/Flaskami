#coding='utf-8'
"""
@:author: Corpoco
@:description: A Flask web service used for cyber security purpose.
               This is a crash test dummy server for your cyber attacks or,
               if you prefer, a server that you can modify and make it more
               strong. The source code is on github: <link da mettere>
"""
from flask import Flask, render_template, request, make_response, jsonify, Response
from flask_restful import Api, Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)
import json
import datetime
import logging


app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'flaskami-'
jwt = JWTManager(app)
app.config['PROPAGATE_EXCEPTIONS'] = True #sposta l'onere della gestione dell'errore



#----------------------------COSTANT------------------------
FLASK_VERSION_ = "1.1.1"
FLASK_RESTFUL_VERSION_ = "0.3.7"
DESCRIPTION_ = "A Flask web service used for cyber security purpose. " \
               "This is a crash test dummy server for you cyber attack, or " \
               ", if you prefer, a server that you can modify and make it more " \
               "strong. The source code is on github: <link da mettere>"

NAME_SERVER_ = "CORPOCO Crash Test Dummy Server: Flaskami"
VERSION_SERVER_ = "1.0.0"

#----------------------------METHOD-------------------------
def hash_password(password):
    return  pwd_context.hash(password)


def verify_password(self, password):
    return pwd_context.verify(password, self.password_hash)

def createToken():
    Identity = ["User", "Admin", "User1"]
    Token = []
    N_token = len(Identity)
    with app.app_context():
        for i in range(0, N_token):
            token = create_access_token(Identity[i])
            Token.append(Token)
            print(f"[!]Token {i}: {token}")
            token = 0;
#----------------------------LOG----------------------------

def start():
    from pyfiglet import Figlet
    custom_fig = Figlet(font='graffiti')
    custom_fig.justify
    print(custom_fig.renderText('FLASKAMI'))
    logging.info(f"[!] {datetime.datetime.now()} ")
    createToken()

@app.before_request
def preRequest():
    if request.script_root == "/JWTApi":
        if "jwt" in request.cookies:
            #return Response(401)
            pass
    #metodo che filtra la richiesta, prevedere db per lo storage delle info
    #per i log usare lo standard log app.logger.info

#----------------------------API----------------------------
#3 simple resource (in the restfull mindset) to test
#1)Home, only for information purpose and contains the API's tree
#2)SimpleApi, a fictive resource without any security control with the HTTP method
#3)JWTApi, a fictive resource reached only with a jwt token

class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)


class SimpleApi(Resource):
    def get(self):
        return {
                "Name":NAME_SERVER_,
                "Auth":"None",
                "Version":VERSION_SERVER_,
                "Time":f"{datetime.datetime.now()}",
                "Server":"Flask server",
                "Flask Version":FLASK_VERSION_,
                "Flask RESTfull Version":FLASK_RESTFUL_VERSION_,
                "Description":DESCRIPTION_
               },200
    def post(self):
        data = request.get_json()
        return {"Name":NAME_SERVER_,
                "Auth":"None",
                "Version":VERSION_SERVER_,
                "Time":f"{datetime.datetime.now()}",
                "status":"POST Gone"
               },200



class JWTApi(Resource):
    @jwt_required
    def get(self):
        if request.headers['Authorization']!=None:
            user = get_jwt_identity() #if none
            return {
                   "Name": NAME_SERVER_,
                   "Auth":"JWT",
                   "Version": VERSION_SERVER_,
                   "Time": f"{datetime.datetime.now()}",
                   "Server": "Flask server",
                   "Flask Version": FLASK_VERSION_,
                   "Flask RESTfull Version": FLASK_RESTFUL_VERSION_,
                   "Description": DESCRIPTION_
                   }, 200
        else:
            return 401
    @jwt_required
    def post(self):
        get_jwt_identity()
        data = request.get_json()
        return {"Name": NAME_SERVER_,
                "Auth":"JWT",
                "Version": VERSION_SERVER_,
                "Time": f"{datetime.datetime.now()}",
                "status": "POST Gone"
                }, 200
    #anche post con argomenti singoli

api.add_resource(Home,"/")
api.add_resource(SimpleApi,"/simpleApi")
api.add_resource(JWTApi,"/JWTApi")


if __name__ == '__main__':
   start()
   logging.warning(f"This is {NAME_SERVER_}, Version {VERSION_SERVER_}")
   #su sistemi ubuntu (testati su 18.04 e 19.04) host="0.0.0.0" per essere visibili nella rete lan, mentre windows vuole l'indirizzo privato
   #prevedere switch
   app.run(host='0.0.0.0',port=5000,debug=False)
   #app.run(host='192.168.1.4',debug = False, port=5000)

"""
da fare
1)Inserire swaggger delle api
2)prevedere un API collegata ad un DB (meglio ancora uno Rel. e uno Non Rel.) per testare anche gli SQL Injection
3) SWAGGER https://github.com/rantav/flask-restful-swagger
"""