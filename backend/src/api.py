import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# @TODO uncomment the following line to initialize the database (DONE)
'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''


# db_drop_and_create_all()


def show_auth_user(jwt):
    if jwt['sub'] == 'auth0|613bd58563762c0070c04279':
        print('MANAGER authenticated!')
    elif jwt['sub'] == 'auth0|613bd6324fec6d00682b27bd':
        print('BARISTA authenticated!')


# ROUTES

# @TODO implement endpoint
#     GET /drinks (DONE)
'''
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} 
    where drinks is the list of drinks or appropriate status code 
    indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.all()

        if len(drinks) == 0:
            abort(404)

        shortened_drinks = [drink.short() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': shortened_drinks,
        })
    except():
        abort(500)


# @TODO implement endpoint
#     GET /drinks-detail (DONE)
'''
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} 
    where drinks is the list of drinks or appropriate status code 
    indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    show_auth_user(jwt)

    try:
        drinks = Drink.query.all()

        if len(drinks) == 0:
            abort(404)

        long_drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': long_drinks
        })
    except():
        abort(500)


# @TODO implement endpoint
#     POST /drinks
'''
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

# @TODO implement endpoint
#     PATCH /drinks/<id>
'''
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} 
    where drink an array containing only the updated drink or appropriate 
    status code indicating reason for failure
'''

# @TODO implement endpoint
#     DELETE /drinks/<id>
'''
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} 
    where id is the id of the deleted record or appropriate status 
    code indicating reason for failure
'''

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# @TODO implement error handlers using the @app.errorhandler(error) decorator
'''
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

# @TODO implement error handler for 404
'''
    error handler should conform to general task above
'''

# @TODO implement error handler for AuthError
'''
    error handler should conform to general task above
'''