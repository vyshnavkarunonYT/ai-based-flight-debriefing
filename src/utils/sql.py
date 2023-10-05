# Handles all the sql based functions
import mysql.connector
import src.utils.constants as CONST
from src.objects.User import User
from src.objects.Platform import  Platform

class SQL():
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Root20@@',
            database='nexus'
        )

        self.cursor = self.db.cursor()

    # auth - Used to authenticate the user
    # Input - username, type and password
    # Returns - None if user not authenticated, otherwise a dictionary of user attributes
    def auth(self, username, type, password):
        # Define default values for when username is not typed - TESTING ONLY
        if username == '':
            username = 'johndoe'
            password = '123'
            type = CONST.USER

        # Creating a prepared statement to perform authentication
        statement = 'select * from auth where username=%s and type=%s and password=%s'

        # Execute the prepared sql query
        self.cursor.execute(statement, [username, type, password])

        result = self.cursor.fetchone()

        # Return a None value if the specific user could not be authenticated
        if result is None:
            print('No match found')
            return None

        # Return a dictionary of user attributes if the specific user was authenticated
        return dict({
            'userID':result[0],
            'username':result[1],
            'type':result[3],
            'firstname':result[4],
            'lastname':result[5]
        })

    # Function that returns a tuple containing a list of users
    # Output returns a list of user objects
    def getUserList(self):
        userList = []

        # Getting the list of users from the database
        statement = 'select * from auth'
        self.cursor.execute(statement)

        for result in self.cursor:
            user = User(result[1], result[3], result[4], result[5])
            userList.append(user)

        return userList


    # Function to create a new user
    def createUser(self, username,password, type, firstname, lastname):
        # Creating the prepared statement to add a new user
        statement = 'insert into auth(username, password, type, firstname, lastname)' \
                    ' values(%s, %s, %s, %s, %s)'

        print('Creating user', username, password, type, firstname, lastname)
        # Execute the prepared sql query
        try:
            self.cursor.execute(statement, [username, password, type, firstname, lastname])
            self.db.commit()
            return 'User Created'
        except:
            print('Unable to create user')
            return None

    # Function to load all platforms
    def getPlatformsList(self):
        # Load Component Dictionary
        components_dict = self.getComponentsDict()
        # Load the platforms list
        platformList = []
        #Getting the list of platforms from the database
        statement = 'select * from platform'
        self.cursor.execute(statement)

        for platform in self.cursor:
            component_keys = platform[3].split(',')
            curr_components = []
            for key in component_keys:
                # Handle the error when no components are present for platform
                # When no components are present split returns one list item that is empty string
                if key == '':
                    break
                curr_components.append(components_dict[int(key)])
            new_platform = Platform(platform[1], platform[2], curr_components)
            platformList.append(new_platform)
        return platformList

    def addPlatform(self, newPlatform):
        # Creating the prepared statement to add a new platform
        statement = 'insert into platform(name, description, components)' \
                    ' values(%s, %s, %s)'

        print('Adding new platform', newPlatform.name, newPlatform.description)
        # Execute the prepared sql query
        try:
            self.cursor.execute(statement, [newPlatform.name, newPlatform.description, ''])
            self.db.commit()
            return 'Platform Added'
        except:
            print('Unable to add platform')
            return None

    # Function to get the first platform
    def getPlatform(self):
        # Load Component Dictionary
        components_dict = self.getComponentsDict()
        # Load the platforms list
        platformList = []
        # Getting the list of platforms from the database
        statement = 'select * from platform limit 1'
        self.cursor.execute(statement)

        for platform in self.cursor:
            component_keys = platform[3].split(',')
            curr_components = []
            for key in component_keys:
                # Handle the error when no components are present for platform
                # When no components are present split returns one list item that is empty string
                if key == '':
                    break
                curr_components.append(components_dict[int(key)])
            new_platform = Platform(platform[1], platform[2], curr_components)
            platformList.append(new_platform)

        return platformList[0]

    # Function to load components as dictionary
    def getComponentsDict(self):
        componentDict = {}
        # Getting the list of components from the database
        statement = 'select * from components'
        self.cursor.execute(statement)
        for result in self.cursor:
            componentDict[result[0]] = result[1]
        return componentDict
