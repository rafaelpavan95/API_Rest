from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from BLACKLIST import BLACKLIST

# CRUD: Create, Read, Update, Delete
#       Post,   Get,  Put,   Delete -> Restful

features = reqparse.RequestParser()

features.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
        
features.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank")

class User(Resource):

    def get(self, user_id):
        
        user = UserModel.find_user(user_id)

        if user is not None:
            
            return user.json()

        else: return {'message': f"User '{user_id}' not found"}, 404 # Not Found

    @jwt_required()
    def delete(self, user_id):

        user = UserModel.find_user(user_id)

        if user:


            try:

                user.delete_user()
            
            except: 

                return {'message': 'An internal error ocurred while trying to delete user.'}, 500 # internal server error
            
            return {'message': f"User '{user_id}' deleted."}

        return {'message': f"User '{user_id}' not found."}, 404 


class UserRegister(Resource):

    def post(self):

        data = features.parse_args()

        if UserModel.find_by_login(data['login']):

            return {'message': f"Login {data['login']} already exists"}

        else: 

            user = UserModel(**data)

            user.save_user()

            return {'message': f"User created successfully"}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):

        data = features.parse_args()

        user = UserModel.find_by_login(data['login'])

        if user and safe_str_cmp(user.password, data['password']):
            
            token = create_access_token(identity=user.user_id)

            return {'access token': token}, 200

        else: return {'message': "login or password is incorrect."}, 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)

        return {'message':'Logout successfully.'}
        