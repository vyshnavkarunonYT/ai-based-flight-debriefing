# Class defintion of Platform
import tkinter as tk
import src.utils.constants as CONST

class Platform():
    # Variables
    name = 'NAME'
    description = 'DESCRIPTION'
    components = []

    def __init__(self, name='NAME', description='DESCRIPTION', components=[]):
        self.name = name
        self.description = description
        self.components = components