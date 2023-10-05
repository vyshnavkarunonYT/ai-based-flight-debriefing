# Main application window python file - Loads other components
import tkinter as tk
from src.screens.Login import Login
from src.screens.UserDashboard import UserDashboard
from src.screens.AdminDashboard import AdminDashboard
import src.utils.constants as CONST
from src.utils.sql import SQL
from src.objects.User import User


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize SQl object to handle sql based functions - auth, getPlatforms, addUser etc
        self.SQL = SQL()
        self.user = User('', '', '', '')

        # Root window configuration
        self.title('Nexus')
        self.geometry('1000x800')

        # Make screens expand and fit the whole frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Login Screen
        self.loginScreen = Login(self)
        self.loginScreen.grid(row=0, column=0, sticky='nsew')
        # Get the username and password from the login screen and use it to authenticate the user
        self.loginScreen.loginBtn['command'] = lambda: self.authenticate(self.loginScreen.username.get(),
                                                                         self.loginScreen.type.get(),
                                                                         self.loginScreen.password.get())

        # Admin Dashboard Screen
        self.adminDashboardScreen = AdminDashboard(self, self.SQL, self.user)
        # Add the logout option to the logout button in AdminDashboard
        self.adminDashboardScreen.logoutBtn['command'] = self.logoutFromDA

        # User Dashboard Screen
        self.userDashboardScreen = UserDashboard(self, self.SQL, self.user)

    # Get the username, type and password from login screen and handle login
    # through sql.Login
    def authenticate(self, username, type, password):
        result = self.SQL.auth(username, type, password)

        # If a user is authenticated load the user data and change screen to adminDashboard
        # or userDashboard depending on the user type

        if result is not None:
            self.user.username = result['username']
            self.user.firstname = result['firstname']
            self.user.lastname = result['lastname']
            self.user.type = result['type']
            # If the user type is admin login to the admin dashboard
            if self.user.type == CONST.ADMIN:
                # Initialize screens
                self.adminDashboardScreen.grid(row=0, column=0, sticky='nsew')
                self.adminDashboardScreen.tkraise()

            # Elif the user type is user login to the user dashboard
            elif self.user.type == CONST.USER:
                print('User login successful')
                self.userDashboardScreen.grid(row=0, column=0, sticky='nsew')
                self.userDashboardScreen.tkraise()

    # Function to logout from admin dashboard when logout button is clicked
    def logoutFromDA(self):
        # Push Login Screen to Top
        self.loginScreen.tkraise()


# Main function
if __name__ == "__main__":
    app = App()
    app.mainloop()
