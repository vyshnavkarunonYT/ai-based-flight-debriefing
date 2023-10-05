# Class defintion of User
import tkinter as tk
import src.utils.constants as CONST

class User():
    # Variables
    username = 'USERNAME',
    type = CONST.USER
    firstname = 'FIRSTNAME'
    lastname = 'LASTNAME'

    def __init__(self, username='USERNAME', type='TYPE', firstname='FIRSNTAME', lastname='LASTNAME'):
        self.username = username
        self.type = type
        self.firstname = firstname
        self.lastname = lastname