from scipy.io import wavfile
import noisereduce as nr
# load data
rate, data = wavfile.read("../../res/audio/Recording.wav")
# perform noise reduction
reduced_noise = nr.reduce_noise(y=data, sr=rate)
wavfile.write("../../res/audio/Recording_nr.wav", rate, reduced_noise)