from sql_alchemy import database
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = ''
MAILGUN_API_KEY = ''
FROM_TITLE = 'Email Validation - No-Reply'
FROM_EMAIL = 'no-reply@restapihoteis.com'


class UserModel(database.Model):
    
    __tablename__ = 'users'

    user_id = database.Column(database.Integer(), primary_key = True)
    login = database.Column(database.String(40))
    password = database.Column(database.String(40),nullable=False)
    email = database.Column(database.String(80), nullable=False, unique=True)
    activated = database.Column(database.Boolean(), default=False)


    def __init__(self, login, password, activated, email) -> None:

        self.login = login
        self.password = password 
        self.activated = activated
        self.email = email

    def json(self):

        return {'user_id': self.user_id,
                'login': self.login,
                'email': self.email,
                'activated': self.activated
                }


    def send_confirmation_email(self):


        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)

        return post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages', 
        auth=('api', MAILGUN_API_KEY), 
        data={'from':f'{FROM_TITLE} <{FROM_EMAIL}>', 'to': self.email, 
        'subject': 'User confirmation', 'text': f'Please, validate your user at: {link}', 'html':[]})

    @classmethod
    def find_user(cls, user_id):

        user = cls.query.filter_by(user_id = user_id).first()
        
        if user:
            return user
        
        return None

    @classmethod
    def find_by_login(cls, login):

        user = cls.query.filter_by(login = login).first()
        
        if user:
            return user
        
        return None

    @classmethod
    def find_by_email(cls, email):

        user = cls.query.filter_by(email = email).first()
        
        if user:
            return user
        
        return None


    def save_user(self):

        database.session.add(self)

        database.session.commit()


    def delete_user(self):
        
        database.session.delete(self)
        
        database.session.commit()
