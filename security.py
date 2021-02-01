# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:36:47 2021

@author: mateo
"""

from werkzeug.security import safe_str_cmp #For safe comparison between str
from user import User

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password , password):
        return user.id
    return None

def identity(userid):
    return User.find_by_id(userid)
    













