from flask import Flask, jsonify
from flask_restful import Api
from BLACKLIST import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from BLACKLIST import BLACKLIST
from resources.site import Site, Sites

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret" 
app.config["JWT_BLACKLIST_ENABLED"] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_database():
    
    database.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):

    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidade(jwt_header, jwt_payload):

    return jsonify({'message': "You have been logged out."}), 401


api.add_resource(Hoteis, '/hoteis')

api.add_resource(Hotel, '/hoteis/<string:id>')

api.add_resource(Sites, '/sites')

api.add_resource(Site, '/sites/<string:url>')

api.add_resource(User, '/usuarios/<int:user_id>')

api.add_resource(UserRegister, '/signin')

api.add_resource(UserLogin, '/login')

api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    
    from sql_alchemy import database
    
    database.init_app(app)
    
    app.run(debug=True)
    