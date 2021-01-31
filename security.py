# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:36:47 2021

@author: mateo
"""

from werkzeug.security import safe_str_cmp #For safe comparison between str
from user import User

users = [ 
    User(1, 'mateo', '12345')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password , password):
        return user.id
    return None

def identity(userid):
    return userid_mapping.get(userid, None)
    













