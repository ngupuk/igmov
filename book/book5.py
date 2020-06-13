# %%
import numpy as np

def get_freq_list():
  certerFreq = np.array([39, 50, 63, 79, 99, 125, 157, 198, 250, 315, 
  397, 500, 630, 794, 1000, 1260, 1588, 2000, 2520, 3176, 4000, 5040, 6352, 8000, 10080, 
  12704, 16000])

  factor = np.power(10, 1.0/6.0)
  lowFreq_Hz = certerFreq/factor;
  highFreq_Hz = certerFreq*factor;

  return np.array(list(zip(lowFreq_Hz, highFreq_Hz)))
get_freq_list()

# %%
import moviepy.editor as mpy
audioPath = '../sample/sample.ogg'
# %%
audio = mpy.AudioFileClip(audioPath)
sound = audio.to_soundarray()[:, 0]
# %%
import matplotlib.pyplot as plt
# %%
sample_sound = sound[1000:150000]
freqs_list = get_freq_list()
fourier = np.fft.rfft(sample_sound)
freqs = np.fft.fftfreq(fourier.shape[0])
plt.plot(np.abs(freqs)*44000, np.abs(fourier))
plt.show()
# %%
np.where(np.logical_and(freqs*44000 <= freqs_list[26, 1], freqs*44000 >= freqs_list[26, 0]))
# %%


def get_result(fourier, freqs, sr=44000):
  freqs_hz = freqs*sr
  results = []
  for band in get_freq_list():
    lower = freqs_hz <= band[1]
    upper = freqs_hz >= band[0]
    indexs = np.where(np.logical_and(lower, upper))
    result = np.average(np.abs(fourier[indexs]))
    results.append(result)
  return np.array(results)

octave = get_result(fourier, freqs)
plt.plot(octave)