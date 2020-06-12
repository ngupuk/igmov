# %%
import numpy as np
from moviepy.editor import *
import matplotlib.pyplot as plt

audioPath = '../sample/sample.ogg'
thumbPath = '../sample/thumb.jpg'
audio = mpy.AudioFileClip(audioPath)
sound = audio.to_soundarray()

fps = 24
sr = sound.shape[0]/audio.duration

def get_sound(t):
  length = 100
  end = sr * t
  start = end - 2*length
  start = 0 if start<0 else start
  L = sound[int(start):int(end), 0]

  hasil = np.fft.fft(L, length)
  freqs = np.fft.fftfreq(length)
  return abs(hasil[:length//2])

# plt.plot(get_sound(2))
# sr