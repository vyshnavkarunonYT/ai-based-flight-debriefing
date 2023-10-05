from pydub import AudioSegment

song = AudioSegment.from_wav('../../res/audio/Recording_nr.wav')

song_25Db_louder = song+25

song_25Db_louder.export('../../res/audio/Recording_nrab.wav', format='wav')