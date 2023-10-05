# AdminDashboardScreen
import tkinter as tk
from src.objects.User import User
import src.utils.constants as CONST
from src.objects.Platform import Platform

class ADPlatform(tk.Frame):
    def __init__(self, parent, SQL, user):

        super().__init__(parent)

        #Variables
        self.SQL = SQL
        self.platformList = []
        self.componentList = []
        self.addPlatformName = tk.StringVar()
        self.actionTitle = tk.StringVar()
        self.actionTitle.set('Edit Platform: None Selected')

        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        # Left Frame
        self.leftFrame = tk.Frame(self, highlightbackground=CONST.LIGHT_GRAY,
                                  highlightthickness=1)
        self.leftFrame.grid(row=0, column=0, sticky='nsew')

        self.leftFrame.columnconfigure(0, weight=1)

        self.leftFrame.rowconfigure(0, weight=0)
        # platformToolBox - Add and Delete platforms
        self.platformToolbox = tk.Frame(self.leftFrame, bg='yellow')
        self.platformToolbox.grid(row=0, column=0, sticky='nsew')

        self.platformToolbox.rowconfigure(0, weight=1)
        self.platformToolbox.columnconfigure(0, weight=5)
        # addPlatformEntry
        self.addPlatformEntry = tk.Entry(self.platformToolbox, font=CONST.BODY_FONT_LARGE,
                                         textvariable=self.addPlatformName)
        self.addPlatformEntry.grid(row=0, column=0, sticky='nsew')

        self.platformToolbox.columnconfigure(1, weight=1)
        # addPlatformBtn
        self.addPlatformBtn = tk.Button(self.platformToolbox, text='+', font = CONST.BODY_FONT_SMALL_BOLD,
                                        command=self.addPlatform, bg='green', fg=CONST.WHITE)
        self.addPlatformBtn.grid(row=0, column=1, sticky='nsew')

        self.platformToolbox.columnconfigure(2, weight=1)
        # deletePlatformBtn
        self.deletePlatformBtn = tk.Button(self.platformToolbox, text='X',
                                           bg='red', fg=CONST.WHITE)
        self.deletePlatformBtn.grid(row=0, column=2, sticky='nsew')

        self.leftFrame.rowconfigure(1, weight=1)
        # Platform List Box
        self.platformListbox = tk.Listbox(self.leftFrame, font=CONST.BODY_FONT_LARGE,
                                          exportselection=False, selectbackground=CONST.BLUE)
        self.platformListbox.insert(0, *self.platformList)
        self.platformListbox.grid(row=1, column=0, sticky='nsew')
        self.platformListbox.bind('<<ListboxSelect>>', self.platformSelected)

        self.columnconfigure(1, weight=3)
        # Right Frame
        self.rightFrame = tk.Frame(self)
        self.rightFrame.grid(row=0, column=1, sticky='nsew')

        self.rightFrame.columnconfigure(0, weight=1)
        self.rightFrame.rowconfigure(0, weight=0)
        # actionTitle Frame - Hold the actionTitleLbl
        self.actionTitleFrame = tk.Frame(self.rightFrame)
        self.actionTitleFrame.grid(row=0, column=0, sticky='nsew')

        self.actionTitleFrame.rowconfigure(0, weight=1)
        self.actionTitleFrame.columnconfigure(0, weight=1)
        # actionTitleLbl- Specify what actions are to be made
        self.actionTitleLbl = tk.Label(self.actionTitleFrame, anchor='nw',textvariable=self.actionTitle,
                                       text=self.actionTitle,font= CONST.BODY_FONT_LARGE_BOLD)
        self.actionTitleLbl.grid(row=0, column=0, sticky='nsew')

        self.rightFrame.rowconfigure(1,weight=1)
        # actionBodyFrame - Holds edit or add new platform components
        self.actionBodyFrame = tk.Frame(self.rightFrame)
        self.actionBodyFrame.grid(row=1, column=0, sticky='nsew')

        self.actionBodyFrame.rowconfigure(0, weight=1)
        self.actionBodyFrame.columnconfigure(0, weight=1)

        # componentsListbox
        self.currComponentsListbox = tk.Listbox(self.actionBodyFrame, font=CONST.BODY_FONT_LARGE,
                                          exportselection=False, selectbackground=CONST.BLUE)
        self.currComponentsListbox.insert(0, *self.componentList)
        self.currComponentsListbox.grid(row=0, column=0, sticky='nsew')


        # Initial Display Data
        self.updatePlatformList() # Fetch the SQL Data
        self.platformListbox.select_set(0)  # Set First Plane by Default
        self.platformSelected(None) # Load the components of the first plane


    def loadPlatformList(self):
        self.platformListbox.delete(0, "end")
        self.platformListbox.insert(0, *[platform.name for platform in self.platformList])

    def updatePlatformList(self):
        self.platformList = self.SQL.getPlatformsList()
        self.loadPlatformList()

    def platformSelected(self, event):
        selected_platform_idx = self.platformListbox.curselection()[0]
        self.currComponentsListbox.delete(0, 'end')
        self.currComponentsListbox.insert(0, *self.platformList[selected_platform_idx].components)
        self.actionTitle.set('Edit Platform: ' + self.platformList[selected_platform_idx].name)
        # print(self.actionTitle)


    def addPlatform(self):
        newPlatform = Platform(self.addPlatformName.get(), "", [])
        # Adding platform to SQL DB
        result = self.SQL.addPlatform(newPlatform)
        if result is None:
            return
        # Update Platform List
        self.updatePlatformList()