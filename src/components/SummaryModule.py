# SummaryModule
import tkinter as tk
import tkinter.ttk as ttk
import src.utils.constants as CONST
from src.components.SummaryCard import SummaryCard

class SummaryModule(tk.Frame):
    def __init__(self, parent, platform):
        super().__init__(parent)

        #Variables
        self.compDesc = None
        self.platform = platform

        # Make all child components to expand to full size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self['highlightbackground'] = CONST.LIGHT_GRAY
        self['highlightthickness'] = 1
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        # TitleFrame - to hold the titleLbl0
        titleFrame = tk.Frame(self, highlightthickness=1, highlightbackground=CONST.LIGHT_GRAY)
        titleFrame.grid(row=0, column=0, sticky='nsew')

        titleFrame.rowconfigure(0, weight=1)
        titleFrame.columnconfigure(0, weight=1)
        # TileLbl - Displays the title 'Summary'
        titleLbl = tk.Label(titleFrame, text='Summary', font=CONST.BODY_FONT_LARGE_BOLD,
                            padx=5, pady=5)
        titleLbl.grid(row=0, column=0, sticky='nw')

        # filterComponentsLbl
        filterComponentsLbl = tk.Label(titleFrame, text='Components: ', font=CONST.BODY_FONT_SMALLEST)
        filterComponentsLbl.grid(row=0, column=1, sticky='e')

        # filterComponentsCB
        # Component Combo Box
        self.filterComponentVal = tk.StringVar()
        self.filterComponentOptions = [CONST.FILTER_VAL_ALL]
        self.filterComponentOptions.extend(platform.components)
        self.filterComponentsCB = ttk.Combobox(titleFrame, width=10,
                                        textvariable=self.filterComponentVal,
                                        state='readonly')
        self.filterComponentsCB.grid(row=0, column=2, sticky='e', padx=(0,5))
        self.filterComponentsCB['values'] = self.filterComponentOptions
        self.filterComponentsCB.current(0)
        self.filterComponentsCB.bind('<<ComboboxSelected>>', self.filterComponentCBSelected)

        self.rowconfigure(1, weight=1)
        # Pre Analysis Frame
        self.preAnalysisFrame = tk.Frame(self, bg=CONST.WHITE)
        self.preAnalysisFrame.grid(row=1, column=0, sticky='nsew')

        self.preAnalysisFrame.columnconfigure(0, weight=1)
        # analysePrompt
        self.analysePrompt = tk.Label(self.preAnalysisFrame, text='Transcript not yet analyzed.',
                                      font=CONST.BODY_FONT_SMALL, bg=CONST.WHITE)
        self.analysePrompt.grid(row=0, column=0, sticky='ew', pady=(20,10))
        # analyseBtn
        self.analyseBtn = tk.Button(self.preAnalysisFrame, text='Analyse', font=CONST.BODY_FONT_SMALL,
                                    bg = CONST.GRAY, fg=CONST.WHITE, state=tk.DISABLED)
        self.analyseBtn.grid(row=1, column=0, pady=(20,0), ipadx=20)

        # Content Frame
        self.contentFrame = tk.Frame(self, bg='white')
        self.contentFrame.grid(row=1, column=0, sticky='nsew')

        self.preAnalysisFrame.tkraise()

    def setCompDesc(self, compDesc):
        self.compDesc = compDesc

    def renderContentFrame(self):
        # Remove all existing children within the content frame
        for child in self.contentFrame.winfo_children():
            child.destroy()
        filteredComponentsList = self.compDesc.keys() if self.filterComponentVal.get()==CONST.FILTER_VAL_ALL else\
            [self.filterComponentVal.get().lower()]
        self.contentFrame.rowconfigure(0, weight=1)
        self.contentFrame.columnconfigure(0, weight=1)
        self.compSummaryCards=[]
        count = 0
        self.contentFrame.columnconfigure(0, weight=1)
        for component in filteredComponentsList:
            compDescList = self.compDesc[component]
            for desc in compDescList:
                self.compSummaryCards.append(SummaryCard(self.contentFrame, component, desc))
                self.contentFrame.rowconfigure(count, weight=0)
                self.compSummaryCards[count].grid(row=count, column=0, sticky='nsew', padx=(5,5), pady=(5,5))
                self.compSummaryCards[count].bind("<Button-1>", self.popDialog)
                count += 1

        self.contentFrame.tkraise()

    def filterComponentCBSelected(self, event):
        print('Selected component was ', self.filterComponentVal.get())
        self.renderContentFrame()


    def popDialog(self, event):
        print('Pop Dialog called')
        tk.messagebox.showinfo("Camera - Blurry", "If you've recently dropped you phone,"
                                                  " check for cracks or scratches."
                                                  " If so, please take it to the nearest service centre.")