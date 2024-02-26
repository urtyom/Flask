from typing import Type

import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from models import User, Session
from schema import CreateUser, UpdateUser

app = Flask('app')
bcrypt = Bcrypt(app )


def hash_password(password: str):
    password = password.encode()
    return bcrypt.generate_password_hash(password).decode()


def check_password(password: str, hashed: str):
    password = password.encode()
    hashed = hashed.encode()
    return bcrypt.check_password_hash(hashed, password)



@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response


def get_user_by_id(user_id):
    user = request.session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, 'user already exist')


def validate_json(json_data: dict, schema_class: Type[CreateUser] | Type[UpdateUser]):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


class UserView(MethodView):

    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data = validate_json(request.json, CreateUser)
        user_data['password'] = hash_password(user_data['password'])
        user = User(**user_data)
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id: int):
        user_data = validate_json(request.json, UpdateUser)
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        user = get_user_by_id(user_id)
        for field, value in user_data.items():
            setattr(user, field, value)
        add_user(user)
        return jsonify(user.dict)

    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({'status': 'deleted'})


UserView = UserView.as_view('user_view')

# def hello_world():
#     print(request.args)
#     print(request.json)
#     print(request.headers)
#     http_response = jsonify({'message': 'Hello world'})
#     http_response.status_code = 201
#     return http_response


app.add_url_rule(
    '/user/<int:user_id>',
    view_func=UserView,
    methods=[
        'PATCH',
        'DELETE'
    ]
)

app.add_url_rule(
    '/user',
    view_func=UserView,
    methods=[
        'POST'
    ]
)

if __name__ == '__main__':
    app.run()
