# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
#JWT standa for JSON web token use for sending encrypted information
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,
    get_jwt_identity)

from security import authenticate, identity

items = [] #Items store 'local databse'

app = Flask(__name__)
app.secret_key = '=jJ-nkyPCE5F|$cy@qz('
api = Api(app)

#An object used to hold JWT settings and callback functions 
jwt = JWTManager(app) 

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
class Login(Resource):
    def post(self):
        request_data = request.get_json() 
        username = request_data.get('username', None)
        password = request_data.get('password', None)
        # Notice that when returning a dictionary jsonify is not longer used 
        # because the api takes care of the conversion.
        if not username:
            return {'message': 'Missing username parameter'}, 400
        if not password:
            return {'message': 'Missing password parameter'}, 400
        
        userid = authenticate(username, password)
        if userid:
            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=userid)
            # By default 200 is send indicating status ok 
            return access_token 
        else:
            # 401 Unauthorized client error status 
            return {'message': 'Bad username or password'}, 401
        
# A resource in REST is a similar Object in Object Oriented Programming or is 
# like an Entity in a Database. Once a resource is identified then its 
# representation is to be decided using a standard format so that the 
# server can send the resource in the above said format and client 
# can understand the same format.
class Item(Resource):
    #Adding and parsing multiple argumnets in a request
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field must be a number and can not be left blank!'
    )
    
    # Protect a view with jwt_required decorator, which requires a valid 
    # access token in the request to access.
    @jwt_required
    def get(self, name):     
        # Access the identity of the current user with get_jwt_identity
        current_userid = get_jwt_identity()    
        if identity(current_userid): 
            item = next(filter(lambda x: (x['item'] == name), items), None)
            # 404 represents status not found
            return {'item': item}, 200 if item else 404 
        else:
            return {'message': 'Bad ID token'}, 401
             
    def post(self, name):        
        if next(filter(lambda x: (x['item'] == name), items),None):
            # status 400 means bad request
            return {'message': f'an item with the name \'{name}\' already exists'}, 400 
        
        request_data = Item.parser.parse_args()
                
        price = request_data['price']
        item = {'item': name, 'price': price}
        items.append(item)
        return item, 201 # status 201 indicates the creation of a new item 
    
    def delete(self, name):
        global items
        size_items_old = items
        items = list(filter(lambda x: x['item'] != name, items))
        size_items_new = items
        if size_items_old == size_items_new:
            return {'message': f'an item with the name \'{name}\' does not exist'}, 400
        else:
            return {'message': f'item with the name \'{name}\' deleted'}
     
    def put(self, name):
        request_data = Item.parser.parse_args()
                
        item = next(filter(lambda x: (x['item'] == name), items),None)
        if item is None:
            price = request_data['price']
            item = {'item': name, 'price': price}
            items.append(item)
        else:
            item.update(request_data)
        return item
        
class Items(Resource):
    def get(self):
        return {'items': items}

#This makes the student class accessible to our API and the endpoint or 
#route is specified in the second parameter
api.add_resource(Login, '/login')
api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:5000/item/name
api.add_resource(Items, '/items')

if __name__ == '__main__':
    app.run(port=5000, debug=True)





