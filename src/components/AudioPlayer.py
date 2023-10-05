# AudioPlayer -
import tkinter as tk
import src.utils.constants as CONST

from tkinter import ttk
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
import time
import threading


class AudioPlayer(tk.Frame):

    def __init__(self, parent, AUDIO_FILE_SOURCE):
        super().__init__(parent)

        # Variables
        self.AUDIO_FILE_SOURCE = AUDIO_FILE_SOURCE
        self.playbackThread = None
        self.startTime = -1
        self.elapsedTime = 0

        self['highlightbackground'] = CONST.LIGHT_GRAY
        self['highlightthickness'] = 1
        self['bg'] = CONST.WHITE
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        # TitleFrame - to hold the titleLbl0
        titleFrame = tk.Frame(self, bg=CONST.WHITE)
        titleFrame.grid(row=0, column=0, sticky='nsew')

        # TileLbl - Displays the title AudioPlayer
        titleLbl = tk.Label(titleFrame, text='Audio Player', font=CONST.BODY_FONT_LARGE_BOLD,
                            padx=5, bg=CONST.WHITE)
        titleLbl.grid(row=0, column=0, sticky='nsew', pady=(5,10))

        self.rowconfigure(1, weight=1)
        # PlayerFrame
        playerFrame = tk.Frame(self, bg=CONST.WHITE)
        playerFrame.grid(row=1, column=0, sticky='nsew', pady=(0,10))
        playerFrame.rowconfigure(0, weight=1)

        playerFrame.columnconfigure(0, weight=0)
        # Rewind Button
        self.rewindBtnImg = tk.PhotoImage(file=CONST.REWIND_BTN_IMAGE_PATH)
        self.rewindBtnImg = self.rewindBtnImg.subsample(2, 2)
        self.rewindBtn = tk.Button(playerFrame, image=self.rewindBtnImg, compound=tk.LEFT,
                                   bg=CONST.BLUE, fg=CONST.WHITE, height=24, width=24,
                                   borderwidth=0)
        self.rewindBtn.grid(row=0, column=0, padx=(10, 0))
        playerFrame.columnconfigure(1, weight=0)

        # PlayButton
        self.playBtnImg = tk.PhotoImage(file=CONST.PLAY_BTN_IMAGE_PATH)
        self.playBtnImg = self.playBtnImg.subsample(2, 2)
        self.playBtn = tk.Button(playerFrame, image=self.playBtnImg, compound=tk.LEFT,
                                 bg=CONST.BLUE, fg=CONST.WHITE, height=24, width=24,
                                 borderwidth=0)
        self.playBtn.grid(row=0, column=1, padx=5)

        playerFrame.columnconfigure(2, weight=1)
        # ProgressBar
        self.progressBar = ttk.Progressbar(playerFrame, orient='horizontal',
                                           mode='determinate')
        self.progressBar.grid(row=0, column=2, padx=10, sticky='ew')
        # Bind the setMusic function to the progress bar click event
        self.progressBar.bind("<Button-1>", self.setMusicPosition)

        # Load the music file
        self.musicFile = self.AUDIO_FILE_SOURCE

        try:
            self.audioData, self.sampleRate = sf.read(self.musicFile)
            self.audioDuration = len(self.audioData) / self.sampleRate
            self.progressBar.configure(maximum=self.audioDuration)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the music file: {str(e)}")

    def play(self):
        self.startTime = time.time()
        sd.play(self.audioData, self.sampleRate, blocking=False)

    def pauseMusic(self):
        sd.stop()

    def resumeMusic(self):
        self.playMusic()

    def updateProgressBar(self):
        try:
            self.elapsedTime = (time.time() - self.startTime)
            self.progressBar['value'] = int(self.elapsedTime)
        except:
            print('sd not started')
        # Update every 100 milliseconds for smoother progress bar animation
        self.progressBar.after(50, self.updateProgressBar)

    def setMusicPosition(self, event):
        # Calculate the new position in seconds based on the mouse click event
        newPosition = event.x / self.progressBar.winfo_width() * self.audioDuration
        # Seek to the desired position
        sd.stop()
        startFrame = int(newPosition * self.sampleRate)
        sd.play(self.audioData[startFrame:], self.sampleRate, blocking=False)
        # Based on the new position, adjust the start time
        self.startTime = self.startTime - (newPosition - self.elapsedTime)
        print(newPosition - self.elapsedTime)

    def playFrom(self, newPosition):
        # Stop the sound device
        sd.stop()

        # Check whether audio player has not been started yet, if not set start time
        if self.startTime == CONST.AUDIO_NOT_STARTED:
            self.startTime = -newPosition
            self.updateProgressBar()

        # Seek to the desired position
        startFrame = int(newPosition * self.sampleRate)
        sd.play(self.audioData[startFrame:], self.sampleRate, blocking=False)
        # Based on the new position adjust the start time
        self.startTime = self.startTime - (newPosition - self.elapsedTime)
