import tkinter as tk
import src.utils.constants as CONST


class SummaryCard(tk.Frame):
    def __init__(self, parent, component, description):
        super().__init__(parent)

        # Variables
        self.description = description
        self['bg'] = CONST.WHITE
        self['highlightbackground'] = CONST.LIGHT_GRAY
        self['highlightthickness'] = 2
        self.rowconfigure(0, weight=1)



        self.columnconfigure(0, weight=1)
        # Render the name of the component
        componentVal = component.capitalize()
        componentVal = "{:<15}".format(componentVal)
        self.componentLbl = tk.Label(self, text=componentVal, anchor='w',
                                     font=CONST.BODY_FONT_SMALL_BOLD, bg='white',
                                     justify='left', width=1)

        self.componentLbl.grid(row=0, column=0, sticky='news', padx=(5,5))

        self.columnconfigure(1, weight=4)
        # Render the sentence
        sentence = self.description['sentence'].strip().capitalize()
        print('SA:', sentence, description['index'])
        info = (sentence[:50]+ '...') if len(sentence) > 50 else sentence.ljust(50)
        self.sentenceLbl = tk.Label(self, text=info, justify='left', width=15,
                                    anchor='w', font = CONST.BODY_FONT_SMALL, bg='white')
        self.sentenceLbl.grid(row=0, column=1, padx=(0,0), sticky='news')
        self.sentenceLbl.bind('<Button-1>', self.popup)
        self.columnconfigure(2, weight=1)
        # Render the sentiment
        sentimentColor = 'green'
        if description['sentiment'] == 'negative':
            sentimentColor = 'red'
        sentimentVal = 'Positive'
        if description['sentiment'] == 'negative':
            sentimentVal = 'Issue'
        sentimentVal = "{:<10}".format(sentimentVal)
        self.sentimentLbl = tk.Label(self, text=sentimentVal, width=1,
                                     fg=sentimentColor, font = CONST.BODY_FONT_SMALLER_BOLD,
                                     anchor='e',justify='left', bg='white')
        self.sentimentLbl.grid(row=0, column=2, sticky='news')

    def popup(self, event):
        print('Clicked')
        tk.messagebox.showinfo("Camera - Blurry", "If you've recently dropped you phone,"
                                                  " check for cracks or scratches."
                                                  " If so, please take it to the nearest service centre.")
