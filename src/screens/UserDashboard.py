# UserDashboardScreen
import tkinter as tk
import src.utils.constants as CONST
from src.components.AudioPlayer import AudioPlayer
from src.components.SummaryModule import SummaryModule
from src.components.DAModule import DAModule
from src.components.TranscriptModule import TranscriptModule
import src.utils.regparser as regparser
import src.utils.sentimentAnalyser as sentAnalyser
import time

import threading

class UserDashboard(tk.Frame):
    def __init__(self, parent, SQL, user):
        # Variables
        AUDIO_FILE_SOURCE = '../../res/audio/complaint.mp3'
        self.projectDescription = tk.StringVar()
        self.platform = SQL.getPlatform()
        self.projectDescription.set(self.platform.name + '/' + '22-06-23')

        super().__init__(parent)

        # Make all child components to expand to full size
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        # Title Frame
        self.titleFrame = tk.Frame(self, highlightthickness=1, highlightbackground=CONST.LIGHT_GRAY)
        self.titleFrame.grid(row=0, column=0, sticky='nsew')

        self.titleFrame.columnconfigure(0, weight=1)
        # Project Description Label - A short project description that serves as title
        self.projectDescriptionLbl = tk.Label(self.titleFrame, text=self.projectDescription.get(),
                                              font=CONST.BODY_FONT_SMALL_BOLD, anchor='nw', justify='left')
        self.projectDescriptionLbl.grid(row=0, column=0, padx=(5, 5), sticky='w')


        self.titleFrame.columnconfigure(1, weight=0)
        # Report Button - Generate a PDF of the report
        self.reportBtn = tk.Button(self.titleFrame, text='Report', font=CONST.BODY_FONT_SMALL_BOLD,
                                   anchor='e', bg=CONST.BLUE,
                                   fg=CONST.WHITE, command=self.generateReport)
        self.reportBtn.grid(row=0, column=1, sticky='nse', pady=5, padx=(0, 10))

        self.titleFrame.columnconfigure(2, weight=0)
        # Logout Button - Used to logout of user dashboard
        self.logoutBtnImg = tk.PhotoImage(file=CONST.LOGOUT_BTN_IMAGE_PATH)
        self.logoutBtnImg = self.logoutBtnImg.subsample(2, 2)
        self.logoutBtn = tk.Button(self.titleFrame, text='Logout', font=CONST.BODY_FONT_SMALL_BOLD,
                                   anchor='e', bg=CONST.GRAY,
                                   fg=CONST.WHITE)
        self.logoutBtn.grid(row=0, column=2, sticky='nse', pady=5, padx=(0, 10))


        self.rowconfigure(1, weight=1)
        # Audio Player Component
        self.audioPlayer = AudioPlayer(self, AUDIO_FILE_SOURCE)
        self.audioPlayer.grid(row=1, column=0, sticky='nsew', pady=(0, 0))
        self.audioPlayer.playBtn.bind('<Button-1>', self.audioPlayBtnClicked)

        self.rowconfigure(2, weight=9)
        # Content Frame
        self.contentFrame = tk.Frame(self, bg='black')
        self.contentFrame.grid(row=2, column=0, sticky='nsew')

        self.contentFrame.rowconfigure(0, weight=1)
        # Summary Module
        self.contentFrame.columnconfigure(0, weight=3)
        self.summaryModule = SummaryModule(self.contentFrame, self.platform)
        self.summaryModule.grid(row=0, column=0, sticky='nsew')
        self.summaryModule.analyseBtn.bind("<Button-1>", self.analyseTranscript)

        # Data Analysis Module
        self.contentFrame.columnconfigure(1, weight=2)
        self.daModule = DAModule(self.contentFrame, self.platform)
        self.daModule.grid(row=0, column=1, sticky='nsew')

        # Transcript Module
        self.contentFrame.columnconfigure(2, weight=1)
        self.transcriptModule = TranscriptModule(self.contentFrame, self.platform, AUDIO_FILE_SOURCE)
        self.transcriptModule.grid(row=0, column=2, sticky='nsew')
        self.transcriptModule.transcriptText.bind("<Double-Button-1>", self.transcriptWordDoubleClicked)
        self.transcriptModule.segmentBtn.bind("<Button-1>", self.setTranscriptAnalyseEnabled)

    def transcriptWordDoubleClicked(self, event):
        index = self.transcriptModule.transcriptText.index(tk.CURRENT)
        tags = self.transcriptModule.transcriptText.tag_names(index)
        if tags:
            clicked_tag = int(tags[0])
            clicked_word_dict = self.transcriptModule.transcript[clicked_tag]
            self.audioPlayer.playFrom(clicked_word_dict['start'])

    def audioPlayBtnClicked(self, event):
        self.audioPlayer.play()
        self.updateProgressBar()

    def updateProgressBar(self):
        try:
            self.audioPlayer.elapsedTime = (time.time() - self.audioPlayer.startTime)
            self.audioPlayer.progressBar['value'] = int(self.audioPlayer.elapsedTime)
        except:
            print('sd not started')
        # Update every 100 milliseconds for smoother progress bar animation
        # self.after(50, lambda: [self.updateProgressBar(),
        #                       self.transcriptModule.liveHighlight(self.audioPlayer.elapsedTime)])
        self.after(50, lambda: [self.updateProgressBar()])

    def setTranscriptAnalyseEnabled(self, event):
        self.summaryModule.analyseBtn.config(bg=CONST.BLUE)
        self.summaryModule.analyseBtn.config(state=tk.NORMAL)

    def analyseTranscript(self, event):
        # Getting the component description dictionary
        print('Available components for platform ', self.platform.name, ' are ', self.platform.components)
        compDesc = regparser.parse(self.transcriptModule.segmentedTranscript, self.platform.components)
        print(compDesc)
        # Get the sentiment analysis of each component
        sentAnalyser.analyseSentiment(compDesc)
        # Set the summary module value to component dictionary
        self.summaryModule.setCompDesc(compDesc)
        # Render the component descriptions
        self.summaryModule.renderContentFrame()

        # Render the overall chart
        self.daModule.renderOverallChart(compDesc)
        # Load the component data
        self.daModule.loadComponentData()
        # Render the component chart
        self.daModule.renderComponentChart()


    def generateReport(self):
        import src.utils.reportGenerator as repGen
        repGen.generateReport(transcript=self.transcriptModule.segmentedTranscript,
                              date='24-06-23',
                              projectName='Project-24/6/23',
                              compDesc=self.summaryModule.compDesc,
                              platform=self.platform.name)