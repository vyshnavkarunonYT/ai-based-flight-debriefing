# TranscriptModule
import tkinter as tk
import src.utils.constants as CONST
import src.utils.speech2text as s2t
import threading
import src.utils.regparser as regparser
import src.utils.sentimentAnalyser as sentAnalyser

class TranscriptModule(tk.Frame):
    def __init__(self, parent, platform, AUDIO_FILE_SOURCE):
        super().__init__(parent)

        # Variables
        self.isSegmented = False
        self.platform = platform
        self.AUDIO_FILE_SOURCE = AUDIO_FILE_SOURCE
        self.transcript = []
        self.transcriptionThread = threading.Thread(target=self.generateTranscriptWithOpenAI)
        self.highlightedTextList = []
        self.segmentedTranscript = 'None'

        # Make all child components to expand to full size
        self.columnconfigure(0, weight=1)
        self['highlightbackground'] = CONST.LIGHT_GRAY
        self['highlightthickness'] = 1

        self.rowconfigure(0, weight=0)
        # TitleFrame - to hold the titleLbl0
        titleFrame = tk.Frame(self)
        titleFrame.grid(row=0, column=0, sticky='nsew')
        titleFrame['highlightbackground'] = CONST.LIGHT_GRAY
        titleFrame['highlightthickness'] = 1

        titleFrame.columnconfigure(0, weight=3)
        # TileLbl - Displays the title AudioPlayer
        titleLbl = tk.Label(titleFrame, text='Transcript', font=CONST.BODY_FONT_LARGE_BOLD,
                            padx=5, pady=5, anchor='w')
        titleLbl.grid(row=0, column=0, sticky='nsew')

        titleFrame.columnconfigure(1, weight=1)
        # Search Entry - Entry to enter search patter in transcript
        self.searchEntry = tk.Entry(titleFrame, font=CONST.BODY_FONT_SMALL, fg=CONST.GRAY)
        self.searchEntry.grid(row=0, column=1, sticky='nsew', padx=(5, 5), pady=(5, 5))
        self.searchEntry.insert(0, 'Enter search query')

        titleFrame.columnconfigure(2, weight=0)
        # Search Button  - Search for a pattern in the generated transcript
        self.searchBtnImg = tk.PhotoImage(file=CONST.SEARCH_BTN_IMAGE_PATH)
        self.searchBtnImg = self.searchBtnImg.subsample(2, 2)
        self.searchBtn = tk.Button(titleFrame, font=CONST.BODY_FONT_SMALL_BOLD,
                                   anchor='e', bg=CONST.BLUE, fg=CONST.WHITE,
                                   image=self.searchBtnImg)
        self.searchBtn.grid(row=0, column=2, sticky='nse', pady=5, padx=(0, 5))

        titleFrame.columnconfigure(3, weight=0)
        # Search Button  - Search for a pattern in the generated transcript
        self.highlightBtnImg = tk.PhotoImage(file=CONST.HIGHLIGHTER_BTN_IMAGE_PATH)
        self.highlightBtnImg = self.highlightBtnImg.subsample(2, 2)
        self.highlightBtn = tk.Button(titleFrame, font=CONST.BODY_FONT_SMALL_BOLD,
                                      anchor='e', bg=CONST.BLUE, fg=CONST.WHITE,
                                      image=self.highlightBtnImg)
        self.highlightBtn.grid(row=0, column=3, sticky='nse', pady=5, padx=(0, 5))

        titleFrame.columnconfigure(4, weight=0)
        # Segment Button - Used to segment the transcript into sentences
        self.segmentBtnImg = tk.PhotoImage(file=CONST.SEGMENT_BTN_IMAGE_PATH)
        self.segmentBtnImg = self.segmentBtnImg.subsample(2, 2)
        self.segmentBtn = tk.Button(titleFrame, font=CONST.BODY_FONT_SMALL_BOLD,
                                    anchor='e', bg=CONST.BLUE, fg=CONST.WHITE,
                                    image=self.segmentBtnImg)
        self.segmentBtn.grid(row=0, column=4, sticky='nse', pady=5, padx=(0, 5))

        titleFrame.columnconfigure(5, weight=0)
        # Generate Button  - Converts the audio file into transcript
        self.generateBtn = tk.Button(titleFrame, text='Generate', font=CONST.BODY_FONT_SMALL_BOLD,
                                     anchor='e', bg=CONST.BLUE, fg=CONST.WHITE,
                                     command=self.transcriptionThread.start)
        self.generateBtn.grid(row=0, column=5, sticky='nse', pady=5, padx=(0, 10))

        self.rowconfigure(1, weight=1)
        # Content Frame
        # transcriptText - To contain the transcripted text
        self.transcriptText = tk.Text(self, padx=5, pady=5, wrap=tk.WORD, font=('Segoe UI', 12), width=50)
        self.transcriptText.grid(row=1, column=0, sticky='nsew')
        self.transcriptText.config(state=tk.DISABLED)

    # Function that calling openAI/Whisper converter to get segmented transcript
    def generateTranscriptWithOpenAI(self):
        # Enable Text before appending words
        self.transcriptText.config(state=tk.NORMAL)
        # Disable generate button
        self.generateBtn.config(state=tk.DISABLED)
        # Display that the text is being generated
        self.transcriptText.insert('insert', 'Generating transcript, please wait...')
        # Get the segmented text from OpenAI/Whisper Library
        self.transcript = s2t.convertWithOpenAI(self.AUDIO_FILE_SOURCE)
        # Remove all the words currently inside text, ie. Generating transcript message
        self.transcriptText.delete('1.0', 'end')
        # Add the obtained transcript to the text
        self.segmentedTranscript = self.transcript['text']
        self.transcriptText.insert('insert', self.segmentedTranscript)
        # Enable generate button
        self.generateBtn.config(state=tk.NORMAL)
        # Disable the text after the transcript has been generated
        self.transcriptText.config(state=tk.DISABLED)
        # Set the isSegment value to true to prevent live highlighting thread
        self.isSegmented = True

    def generateTranscript(self):
        # Enable Text before appending words
        self.transcriptText.config(state=tk.NORMAL)
        # Disable generate button
        self.generateBtn.config(state=tk.DISABLED)
        # Display that the text is being generated
        self.transcriptText.insert('insert', 'Generating transcript, please wait...')
        # Converting the audio file to transcript
        self.transcript = s2t.convert(self.AUDIO_FILE_SOURCE)
        # Remove all the words currently inside text, ie. Generating transcript message
        self.transcriptText.delete('1.0', 'end')
        # Append the gnerate transcript to the text
        for idx, item in enumerate(self.transcript):
            self.transcriptText.insert("end", item['word'] + ' ', idx)
        # Enable generate button
        self.generateBtn.config(state=tk.NORMAL)
        # Disable the text after the transcript has been generated
        self.transcriptText.config(state=tk.DISABLED)
    ''' 
    def segmentTranscript(self):
        self.transcriptText.config(state=tk.NORMAL)
        # Remove all the words currently inside text, ie. Generating transcript message
        self.transcriptText.delete('1.0', 'end')
        # Inform the user that the text is being segmented
        self.transcriptText.insert('insert', 'Text is being segmentation. Please hold..')

        # Convert the transcript into one combined chunk of text
        rawText = ''
        for item in self.transcript:
            rawText = rawText + item['word'] + ' '
        rawText = rawText.strip()

        # Pass the raw text to segmenter and get sentences
        self.segmentedTranscript = segmenter.segment(rawText)
        print(self.segmentedTranscript)

        # Insert the segmented text as the transcript text
        self.transcriptText.delete('1.0', 'end')
        self.transcriptText.insert('insert', self.segmentedTranscript)
        self.transcriptText.config(state=tk.DISABLED)

        # Setting the isSegmented Variable to true, to stop live highlighting
        self.isSegmented = True


    def liveHighlight(self, currTime):
        # Pop all currently highlighted words in the highlighted list and remove highlights

        if len(self.transcript) > 0 and not self.isSegmented:
            # Perform binary search to locate word to highlight
            l = 0
            u = len(self.transcript)
            found = False
            count = 0
            while l < u and count < 10:
                m = (l + u) // 2
                if self.transcript[m]['start'] <= currTime <= self.transcript[m]['end']:
                    found = True
                    break;
                elif self.transcript[m]['start'] >= currTime:
                    u = m - 1
                else:
                    l = m + 1
                count += 1
            if found:
                # Pop all highlighted components so far
                while len(self.highlightedTextList) > 0:
                    rem_idx = self.highlightedTextList.pop()
                    self.transcriptText.tag_config(rem_idx, background="white", foreground="black")
                # Append current word
                self.highlightedTextList.append(m)
                print(currTime, 'Word to highlight is ', self.transcript[m])
                self.transcriptText.tag_config(m, background=CONST.BLUE, foreground=CONST.WHITE)
                # If previous word was withing window, highlight it
                if m > 0 and currTime - self.transcript[m - 1]['end'] < .50:
                    self.highlightedTextList.append(m - 1)
                    self.transcriptText.tag_config(m - 1, background=CONST.BLUE, foreground=CONST.WHITE)
                if m < len(self.transcript) and self.transcript[m + 1]['start'] - currTime < .50:
                    self.highlightedTextList.append(m + 1)
                    self.transcriptText.tag_config(m + 1, background=CONST.BLUE, foreground=CONST.WHITE)
    '''