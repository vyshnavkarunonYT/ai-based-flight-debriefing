# DAModule
import tkinter as tk
from tkinter import ttk
import src.utils.constants as CONST
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

class DAModule(tk.Frame):
    def __init__(self, parent, platform):
        super().__init__(parent)

        # Variables
        self.platform = platform
        self.componentChartsYCol = 1
        self.compDF = None
        self.columnconfigure(0, weight=1)
        self['highlightbackground'] = CONST.LIGHT_GRAY
        self['highlightthickness'] = 1

        self.rowconfigure(0, weight=0)
        # TitleFrame - to hold the titleLbl0
        titleFrame = tk.Frame(self, highlightthickness=1, highlightbackground=CONST.LIGHT_GRAY)
        titleFrame.grid(row=0, column=0, sticky='nsew')

        # TileLbl - Displays the title AudioPlayer
        titleLbl = tk.Label(titleFrame, text='Data Analysis', font=CONST.BODY_FONT_LARGE_BOLD,
                            padx=5, pady=5)
        titleLbl.grid(row=0, column=0, sticky='nsew')

        self.rowconfigure(1, weight=1)
        # Content Frame - To Display the charts
        self.contentFrame = tk.Label(self, bg=CONST.LIGHTEST_GRAY)
        self.contentFrame.grid(row=1, column=0, sticky='nsew')

        self.contentFrame.columnconfigure(0, weight=1)
        self.contentFrame.rowconfigure(0, weight=1)
        # Overall Charts Container
        self.overallChartsContainer = tk.Frame(self.contentFrame, bg=CONST.WHITE, pady=2, padx=2,
                                               highlightbackground=CONST.LIGHT_GRAY, highlightthickness=2)
        self.overallChartsContainer.grid(row=0, column=0, sticky='nsew')

        self.overallChartsContainer.columnconfigure(0, weight=1)

        # Overall Charts Title Frame
        self.overallChartsTitleFrame = tk.Frame(self.overallChartsContainer, highlightthickness=1,
                                                highlightbackground=CONST.LIGHTEST_GRAY, bg=CONST.WHITE)
        self.overallChartsTitleFrame.grid(row=0, column=0, sticky='nsew')

        # Overall Charts Title
        self.overallChartsTitle = tk.Label(self.overallChartsTitleFrame, text='Overall', bg='white', font=CONST.BODY_FONT_SMALL_BOLD)
        self.overallChartsTitle.grid(row=0, column=0, sticky='nsew')

        self.contentFrame.rowconfigure(1, weight=1)

        self.overallChartsContainer.rowconfigure(1, weight=1)
        # Overall Charts Frame
        self.overallChartsFrame = tk.Frame(self.overallChartsContainer, bg=CONST.WHITE)
        self.overallChartsFrame.grid(row=1, column=0, sticky='nsew')

        # Component Charts Container
        self.componentChartsContainer = tk.Frame(self.contentFrame, bg=CONST.WHITE, pady=2, padx=2,
                                               highlightbackground=CONST.LIGHT_GRAY, highlightthickness=2)
        self.componentChartsContainer.grid(row=1, column=0, sticky='nsew')

        self.componentChartsContainer.columnconfigure(0, weight=1)
        # Component Charts Title Frame
        self.componentChartsTitleFrame = tk.Frame(self.componentChartsContainer, highlightthickness=1,
                                                highlightbackground=CONST.LIGHTEST_GRAY, bg=CONST.WHITE)
        self.componentChartsTitleFrame.grid(row=0, column=0, sticky='nsew')

        # Component Charts Title
        self.componentChartsTitle = tk.Label(self.componentChartsTitleFrame, text='Component', bg='white', font=CONST.BODY_FONT_SMALL_BOLD)
        self.componentChartsTitle.grid(row=0, column=0, sticky='nsew')

        self.componentChartsTitleFrame.columnconfigure(1, weight=1)
        # Component Combo Box
        self.selectedComponent = tk.StringVar()
        self.componentCB = ttk.Combobox(self.componentChartsTitleFrame, width=10,
                                        textvariable=self.selectedComponent,
                                        state='readonly')
        self.componentCB.grid(row=0, column=1, sticky='e', padx=(0,5))
        self.componentCB['values'] = self.platform.components
        self.componentCB.current(0)


        # Segment Button - Used to segment the transcript into sentences
        self.nextBtnImg = tk.PhotoImage(file=CONST.NEXT_BTN_IMAGE_PATH)
        self.nextBtnImg = self.nextBtnImg.subsample(2, 2)
        self.nextCompGraphBtn = tk.Button(self.componentChartsTitleFrame, font=CONST.BODY_FONT_SMALL_BOLD,
                                    anchor='e', bg=CONST.BLUE, fg=CONST.WHITE,
                                    image=self.nextBtnImg, command=self.yAxisColChanged)
        self.nextCompGraphBtn.grid(row=0, column=3, sticky='nse', pady=5, padx=(0, 5))



        self.componentChartsContainer.rowconfigure(1, weight=1)
        # Component Charts Frame
        self.componentChartsFrame = tk.Frame(self.componentChartsContainer, bg=CONST.WHITE)
        self.componentChartsFrame.grid(row=1, column=0, sticky='nsew')


    def renderOverallChart(self, compDesc):
        split = [len(compDesc[component]) for component in compDesc]
        fig = Figure(figsize=(1,1))  # create a figure object
        ax = fig.add_subplot(111)  # add an Axes to the figure
        ax.pie(split, radius=1, labels=compDesc.keys(), autopct='%0.2f%%', shadow=True,)
        chart1 = FigureCanvasTkAgg(fig, self.overallChartsFrame)
        # canvas1.pack(side="top", fill='both', expand=True)
        chart1.get_tk_widget().pack(side='top', fill='both', expand=True)

    def loadComponentData(self):
        # Read the excel path to the engine data sheet
        self.compDF = pd.read_excel(CONST.ENGINE_DATA_EXCEL_PATH, sheet_name=CONST.ENGINE_DATA_SHEET)
        # Preprocess the time column so graphs can be plotted
        self.compDF['Time'] = self.compDF['Time'].astype(str)

    def renderComponentChart(self):
        # Remove all child components of components charts frame
        for child in self.componentChartsFrame.winfo_children():
            child.destroy()
        # Get the column title of the Y axis variable
        YTitle = self.compDF.keys()[self.componentChartsYCol]
        fig = Figure(figsize=(1,1))  # create a figure object
        ax = fig.add_subplot(111)  # add an Axes to the figure
        ax.plot(self.compDF.iloc[:,0], self.compDF.iloc[:,self.componentChartsYCol])
        ax.set_title(YTitle, fontsize=10)
        ax.set_xticks(ticks=[i for i in range(0, 30)])
        ax.tick_params(axis='y', labelsize=6)
        ax.tick_params(axis='x', labelsize=4)
        ax.set_xticklabels(labels=[i for i in range(0,30)])
        chart1 = FigureCanvasTkAgg(fig, self.componentChartsFrame)
        # canvas1.pack(side="top", fill='both', expand=True)
        chart1.get_tk_widget().pack(side='top', fill='both', expand=True, pady=2, padx=2)

    def yAxisColChanged(self):
        nCols = len(self.compDF.keys())-1
        print('Params', self.componentChartsYCol, nCols)
        self.componentChartsYCol = (self.componentChartsYCol%nCols)+1
        self.renderComponentChart()
