# Login Screen
# Choose between admin or user login
# Entry box to accept username and password for login
import tkinter as tk
import src.utils.constants as CONST


class Login(tk.Frame):
    def __init__(self, parent):
        super().__init__()

        # Variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.type = tk.StringVar()
        self.type.set(CONST.USER)

        # Make all child components expand to full size
        self.columnconfigure(0, weight=1)

        # titleFrame to hold the title label
        self.rowconfigure(0, weight=1)
        titleFrame = tk.Frame(self, highlightbackground=CONST.DARK_GRAY,
                              highlightthickness=1)
        titleFrame.grid(row=0, column=0, sticky='nsew')

        # titleLabel to display the title - App Name
        titleFrame.rowconfigure(0, weight=1)
        titleFrame.columnconfigure(0, weight=1)
        title = tk.Label(titleFrame, text=CONST.APP_NAME,
                         anchor='center', font=CONST.TITLE_FONT, bg=CONST.WHITE)
        title.grid(row=0, column=0, sticky='nsew')

        # bodyFrame to hold the loginFrame
        self.rowconfigure(1, weight=9)
        bodyFrame = tk.Frame(self, bg=CONST.WHITE)
        bodyFrame.grid(row=1, column=0, sticky='nsew')

        # loginFrame to hold the login components
        bodyFrame.rowconfigure(0, weight=1)
        bodyFrame.rowconfigure(1, weight=2)
        bodyFrame.columnconfigure(0, weight=3)
        bodyFrame.columnconfigure(1, weight=2)
        bodyFrame.columnconfigure(2, weight=3)
        loginFrame = tk.Frame(bodyFrame, highlightbackground=CONST.DARK_GRAY, highlightthickness=1,
                              borderwidth=30, bg=CONST.WHITE)
        loginFrame.grid(row=0, column=1, pady=20, padx=20, ipadx=20, ipady=20)
        loginFrame.columnconfigure(0, weight=1)

        # loginTitle - literal label that says 'Login'
        loginFrame.rowconfigure(0, weight=1)
        loginTitle = tk.Label(loginFrame, text='Login', anchor='center',
                              font=CONST.SUBTITLE_FONT, bg=CONST.WHITE)
        loginTitle.grid(row=0, column=0, sticky='nsew')

        # Frame to hold the user login and admin login toggle buttons
        loginFrame.rowconfigure(1, weight=1)
        uaToggleFrame = tk.Frame(loginFrame, pady=20, bg='white')
        uaToggleFrame.grid(row=1, column=0, sticky='nsew')

        uaToggleFrame.rowconfigure(0, weight=1)
        # userToggleBtn - to select the user login
        uaToggleFrame.columnconfigure(0, weight=1)
        self.userToggleBtn = tk.Button(uaToggleFrame, text='User', font=CONST.BODY_FONT_LARGE_BOLD,
                                       relief=tk.SUNKEN, bg=CONST.BLUE, fg=CONST.WHITE,
                                       command=self.userToggleBtnClicked)
        self.userToggleBtn.grid(row=0, column=0, sticky='nsew')

        # adminToggleBtn - to select the admin login
        uaToggleFrame.columnconfigure(1, weight=1)
        self.adminToggleBtn = tk.Button(uaToggleFrame, bg=CONST.LIGHT_GRAY, relief=tk.FLAT,
                                        text='Admin', font=CONST.BODY_FONT_LARGE_BOLD,
                                        command=self.adminToggleBtnClicked)
        self.adminToggleBtn.grid(row=0, column=1, sticky='nsew')

        # usernameLbl - literal label that says 'Username'
        loginFrame.rowconfigure(2, weight=1)
        usernameLbl = tk.Label(loginFrame, pady=5, text='Username', anchor='nw',
                               font=CONST.BODY_FONT_LARGE, bg='white')
        usernameLbl.grid(row=2, column=0, sticky='nsew')

        # usernameEntry - to enter the username
        loginFrame.rowconfigure(3, weight=1)
        usernameEntry = tk.Entry(loginFrame, relief=tk.SUNKEN, textvariable=self.username,
                                 font=CONST.BODY_FONT_LARGE, bg=CONST.LIGHTEST_GRAY)
        usernameEntry.grid(row=3, column=0, sticky='nsew')

        # passwordLbl - literal label that says 'Password'
        loginFrame.rowconfigure(4, weight=1)
        passwordLbl = tk.Label(loginFrame, pady=5, text='Password', anchor='nw',
                               font=CONST.BODY_FONT_LARGE, bg=CONST.WHITE)
        passwordLbl.grid(row=4, column=0, sticky='nsew')

        # passwordEntry - to enter the password
        loginFrame.rowconfigure(5, weight=1)
        passwordEntry = tk.Entry(loginFrame, relief=tk.SUNKEN, textvariable=self.password,
                                 font=CONST.BODY_FONT_LARGE, show='*', bg=CONST.LIGHTEST_GRAY)
        passwordEntry.grid(row=5, column=0, sticky='nsew')

        # Add an empty row between the last entry and the login button for spacing
        loginFrame.rowconfigure(6, minsize=30)

        # loginBtn - to log into the account
        loginFrame.rowconfigure(7, weight=1, pad=20)
        self.loginBtn = tk.Button(loginFrame, text='Login', padx=100, anchor='center',
                                  font=CONST.BODY_FONT_LARGE_BOLD, fg=CONST.WHITE, bg=CONST.BLUE)
        self.loginBtn.grid(row=7, column=0)

    def userToggleBtnClicked(self):
        self.userToggleBtn['bg'] = CONST.BLUE
        self.userToggleBtn['fg'] = CONST.WHITE
        self.userToggleBtn['relief'] = tk.SUNKEN
        self.adminToggleBtn['bg'] = CONST.LIGHT_GRAY
        self.adminToggleBtn['fg'] = CONST.BLACK
        self.adminToggleBtn['relief'] = tk.FLAT
        self.type.set(CONST.USER)

    def adminToggleBtnClicked(self):
        self.adminToggleBtn['bg'] = CONST.BLUE
        self.adminToggleBtn['fg'] = CONST.WHITE
        self.adminToggleBtn['relief'] = tk.SUNKEN
        self.userToggleBtn['bg'] = CONST.LIGHT_GRAY
        self.userToggleBtn['fg'] = CONST.BLACK
        self.userToggleBtn['relief'] = tk.FLAT
        self.type.set(CONST.ADMIN)
