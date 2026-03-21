from flask import Flask, session, render_template, request, redirect
from flask_restful import Resource, Api
import os
from app.views.password_authenticator import auth 
from app.models.constants import RESOURCES 
from flask_cors import CORS
from app.config.env import EnvConfig

app =  Flask(__name__)
CORS(app)
app.secret_key = EnvConfig.secret_key

# Registers Authorization Handlers
app.register_blueprint(auth, url_prefix=RESOURCES.AUTH.MAIN)

class Main(Resource):
    def get(self):
        return 'Hello!!!'

if  __name__ == '__main__':
    app.run(
        debug=True, 
        host=EnvConfig.host_name,
        port=int(os.environ.get(
                'PORT', 
                EnvConfig.port) 
            )
    )