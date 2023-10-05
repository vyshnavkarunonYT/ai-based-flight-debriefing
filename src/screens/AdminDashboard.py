# AdminDashboardScreen
import tkinter as tk
import src.utils.constants as CONST
from src.components.ADPlatform import ADPlatform


class AdminDashboard(tk.Frame):
    def __init__(self, parent, SQL, user):
        super().__init__()

        # Variables
        self.title = tk.StringVar()
        self.title.set(CONST.AD_USER)
        self.SQL = SQL
        self.userList = []

        # ADUserForm Variables
        self.ADUsernameVal = tk.StringVar()
        self.ADPasswordVal = tk.StringVar()
        self.ADFirstnameVal = tk.StringVar()
        self.ADLastnameVal = tk.StringVar()
        self.ADUserTypeVal = tk.IntVar()

        # The current user (admin)
        self.user = user
        self.username = tk.StringVar()
        self.firstname = tk.StringVar()
        self.username.set(self.user.username)
        self.firstname.set(self.user.firstname)

        # Formatting the look of the frame
        self['highlightbackground'] = CONST.GRAY
        self['highlightthickness'] = 1

        # Child components resize to fit whole AdminDashboard Frame
        self.rowconfigure(0, weight=1)

        # List of drawer options
        self.drawerOptions = ['User', 'Platform']

        # Left Frame
        self.columnconfigure(0, weight=1)
        leftFrame = tk.Frame(self, bg=CONST.BLUE, highlightbackground=CONST.DARK_GRAY, highlightthickness=1)
        leftFrame.grid(row=0, column=0, sticky='nsew')
        leftFrame.columnconfigure(0, weight=1)

        # Left Upper Frame - Details Frame
        leftFrame.rowconfigure(0, weight=1)
        detailsFrame = tk.Frame(leftFrame)
        # detailsFrame.grid(row=0, column=0, sticky='nsew')

        detailsFrame.columnconfigure(0, weight=1)
        # firstnameLbl - To display the admin username
        detailsFrame.rowconfigure(0, weight=0)
        firstnameLbl = tk.Label(detailsFrame, textvariable=self.firstname,
                                text=self.firstname, font=CONST.BODY_FONT_LARGE_BOLD)
        firstnameLbl.grid(row=0, column=0, sticky='nsew')

        # usernameLbl - To display the admin firstname
        detailsFrame.rowconfigure(1, weight=1)
        usernameLbl = tk.Label(detailsFrame, textvariable=self.username, font=CONST.BODY_FONT_SMALL)
        usernameLbl.grid(row=1, column=0, sticky='nsew')

        # Left Lower Frame - Drawer Frame
        # leftFrame.rowconfigure(1, weight=4)
        self.drawerFrame = tk.Frame(leftFrame)
        self.drawerFrame.grid(row=0, column=0, sticky='nsew')
        self.drawerFrame.rowconfigure(0, weight=1)
        self.drawerFrame.columnconfigure(0, weight=1)

        # logoutBtn
        leftFrame.rowconfigure(1, weight=0)
        self.logoutBtn = tk.Button(leftFrame, bg=CONST.LIGHT_GRAY, font=CONST.BODY_FONT_SMALL_BOLD,
                              text='Logout', padx=5, pady=5)
        self.logoutBtn.grid(row=1, column=0, sticky='nsew')

        # Drawer Options Listbox
        self.drawerOptionsListbox = tk.Listbox(self.drawerFrame, font=CONST.BODY_FONT_LARGE_BOLD, exportselection=False,
                                               bg=CONST.LIGHT_GRAY, selectbackground=CONST.BLUE)
        self.drawerOptionsListbox.insert(0, *self.drawerOptions)
        self.drawerOptionsListbox.grid(row=0, column=0, sticky='nsew')
        self.drawerOptionsListbox.select_set(0)  # Set user option to be selected by default
        self.drawerOptionsListbox.bind('<<ListboxSelect>>', self.drawerOptionSelected)

        # Right Frame - Content Frame
        self.columnconfigure(1, weight=14)
        self.rightFrame = tk.Frame(self, bg='black')
        self.rightFrame.grid(row=0, column=1, sticky='nsew')

        self.rightFrame.columnconfigure(0, weight=1)

        # TitleFrame - Holds the title label
        self.rightFrame.rowconfigure(0, weight=1)
        self.titleFrame = tk.Frame(self.rightFrame, highlightbackground=CONST.LIGHT_GRAY,
                             highlightthickness=2)
        self.titleFrame.grid(row=0, column=0, sticky='nsew')

        # TitleLbl - Display the title of the page
        self.titleFrame.rowconfigure(0, weight=1)
        self.titleFrame.columnconfigure(0, weight=1)
        self.titleLbl = tk.Label(self.titleFrame, textvariable = self.title, font=CONST.TITLE_FONT)
        self.titleLbl.grid(row=0, column=0, sticky='nsew')

        # ADUserFrame - Add new users with username and password, Edit current user list
        self.rightFrame.rowconfigure(1, weight=14)
        self.ADUserFrame = tk.Frame(self.rightFrame)
        self.ADUserFrame.grid(row=1, column=0, sticky='nsew')

        self.ADUserFrame.rowconfigure(0, weight=1)
        # ADUserLBFrame - Contains the list of the current users
        self.ADUserFrame.columnconfigure(0, weight=1)
        self.ADUserLBFrame = tk.Frame(self.ADUserFrame)
        self.ADUserLBFrame.grid(row=0, column=0, sticky='nsew')

        # ADUserLB - Contains a list of the current users
        self.ADUserLBFrame.columnconfigure(0, weight=1)
        self.ADUserLBFrame.rowconfigure(0, weight=1)
        self.ADUSerLB = tk.Listbox(self.ADUserLBFrame, font=CONST.BODY_FONT_LARGE, selectbackground=CONST.BLUE)
        self.ADUSerLB.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.loadUserList()

        # ADUserFormFrame - Contains the form like components for adding a new user
        self.ADUserFrame.columnconfigure(1, weight=3)
        self.ADUserFormFrame = tk.Frame(self.ADUserFrame)
        self.ADUserFormFrame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.ADUserFormFrame.columnconfigure(0, weight=1)

        # ADCreateUserTitle
        self.ADUserCreateUserTitle = tk.Label(self.ADUserFormFrame, text='Create New User', anchor='nw',
                                              font=CONST.BODY_FONT_LARGE_BOLD)
        self.ADUserCreateUserTitle.grid(row=0, column=0, sticky='nsew')

        # ADUsernameLbl
        self.ADUsernameLbl = tk.Label(self.ADUserFormFrame, text='Username', anchor='w', font=CONST.BODY_FONT_SMALL_BOLD)
        self.ADUsernameLbl.grid(row=1, column=0, sticky='nsew')

        # ADUsernameEntry - Enter the name of new user
        self.ADUsernameEntry = tk.Entry(self.ADUserFormFrame, font=CONST.BODY_FONT_SMALL,
                                        textvariable=self.ADUsernameVal)
        self.ADUsernameEntry.grid(row=2, column=0, sticky='nsew')

        # ADFirstnameLbl
        self.ADFirstnameLbl = tk.Label(self.ADUserFormFrame, text='Firstname', anchor='w', font=CONST.BODY_FONT_SMALL_BOLD)
        self.ADFirstnameLbl.grid(row=3, column=0, sticky='nsew')

        # ADFirstnameEntry - Enter the name of new user
        self.ADFirstnameEntry = tk.Entry(self.ADUserFormFrame, font=CONST.BODY_FONT_SMALL,
                                         textvariable=self.ADFirstnameVal)
        self.ADFirstnameEntry.grid(row=4, column=0, sticky='nsew')

        # ADLastnameLbl
        self.ADLastnameLbl = tk.Label(self.ADUserFormFrame, text='Lastname', anchor='w', font=CONST.BODY_FONT_SMALL_BOLD)
        self.ADLastnameLbl.grid(row=5, column=0, sticky='nsew')

        # ADLastnameEntry - Enter the name of new user
        self.ADLastnameEntry = tk.Entry(self.ADUserFormFrame, font=CONST.BODY_FONT_SMALL,
                                        textvariable=self.ADLastnameVal)
        self.ADLastnameEntry.grid(row=6, column=0, sticky='nsew')

        # ADPasswordLbl
        self.ADPasswordLbl = tk.Label(self.ADUserFormFrame, text='Password', anchor='w', font=CONST.BODY_FONT_SMALL_BOLD)
        self.ADPasswordLbl.grid(row=7, column=0, sticky='nsew')

        # ADPasswordEntry - Enter the name of new user
        self.ADPasswordEntry = tk.Entry(self.ADUserFormFrame, show='*', font=CONST.BODY_FONT_SMALL,
                                        textvariable=self.ADPasswordVal)
        self.ADPasswordEntry.grid(row=8, column=0, sticky='nsew')

        # ADPasswordLbl
        self.ADConfirmPasswordLbl = tk.Label(self.ADUserFormFrame, text='Confirm Password', anchor='w', font=CONST.BODY_FONT_SMALL_BOLD)
        self.ADConfirmPasswordLbl.grid(row=9, column=0, sticky='nsew')

        # ADPasswordEntry - Enter the name of new user
        self.ADConfirmPasswordEntry = tk.Entry(self.ADUserFormFrame, show='*', font=CONST.BODY_FONT_SMALL)
        self.ADConfirmPasswordEntry.grid(row=10, column=0, sticky='nsew')


        # ADUsertTypeLbl
        self.ADUserTypeLbl = tk.Label(self.ADUserFormFrame, text='User Type', anchor='w',
                                             font=CONST.BODY_FONT_SMALL_BOLD)
        self.ADUserTypeLbl.grid(row=11, column=0, sticky='nsew')


        # ADUserTypeRadioButtons - Get the type of user for account creation

        for text, value in [('User', 1), ('Admin', 2)]:
            tk.Radiobutton(self.ADUserFormFrame, text=text, value=value, variable=self.ADUserTypeVal,
                           anchor='nw', font=CONST.BODY_FONT_SMALL).grid(row=11+value, column=0, sticky='nsew')
        self.ADUserTypeVal.set(1)


        # ADCreateUserBtn - Button to create user
        self.ADCreateUserBtn = tk.Button(self.ADUserFormFrame, text='Create User',
                                         fg='white', bg=CONST.BLUE, anchor='center',
                                         font=CONST.BODY_FONT_SMALL, command = self.createUser)
        self.ADCreateUserBtn.grid(row=14, column=0, sticky='ns', ipadx=100 )

        # ADPlaform - Frame that handles platform level actions
        self.ADPlatformFrame = ADPlatform(self.rightFrame, self.SQL, self.user)
        self.ADPlatformFrame.grid(row=1, column=0, sticky='nsew')

        # Keep the UserFrame page the topmost drawer selection at the start
        self.ADUserFrame.tkraise()

    # Function to handle draweer option selection events - Loads corresponding page
    def drawerOptionSelected(self, event):
        # Return if no drawer option was selected
        if len(self.drawerOptionsListbox.curselection()) == 0:
            print('Drawer Unselected')
            return
        # Get the selected drawer option
        selectedOption = self.drawerOptions[self.drawerOptionsListbox.curselection()[0]]

        # Handle the corresponding event for the selected option
        if selectedOption == CONST.AD_USER:
            # Loading the user frame
            self.title.set(CONST.AD_USER)
            self.loadUserList()
            self.ADUserFrame.tkraise()

        if selectedOption == CONST.AD_PLATFORM:
            # Push platform frame to Top
            self.title.set(CONST.AD_PLATFORM)
            self.ADPlatformFrame.tkraise()


    # Function to refresh the user list
    def loadUserList(self):
        self.userList = self.SQL.getUserList()
        self.ADUSerLB.delete(0, "end")
        self.ADUSerLB.insert(0, *[user.username for user in self.userList])

    # Function to call SQL.createUser and add user to DB
    def createUser(self):
        # Get the type of user to be created
        type = CONST.USER
        if self.ADUserTypeVal==2:
            type = CONST.ADMIN
        # Call the createUser SQL function to create new user and commit to DB -
        # Function returns "User created" on successful user creation else None
        result = self.SQL.createUser(self.ADUsernameVal.get(), self.ADPasswordVal.get(),
                            type, self.ADFirstnameVal.get(), self.ADLastnameVal.get())
        # Reload the user list when a new user is created
        if result is not None:
            self.loadUserList()


    def logout(self):
        print('Logging out')
