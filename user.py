# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:58:42 2021

@author: mateo
"""

import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username = ?"
        # The parameters passed to execute, even if it is a single one, 
        # have to be in a tuple
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        
        # We do NOT have to commit (save) because we did not make any change 
        # to the Database we just retrieve data
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id = ?"
        # The parameters passed to execute, even if it is a single one, 
        # have to be in a tuple
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        
        # We do NOT have to commit (save) because we did not make any change 
        # to the Database we just retrieve data
        connection.close()
        return user
        
        
    