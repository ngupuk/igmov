# %%
import numpy as np
import moviepy.editor as mpy
import cv2
import igmov.analizer

audioPath = '../sample/sample.ogg'
thumbPath = '../sample/thumb.jpg'

# %%
audio = mpy.AudioFileClip(audioPath)
thumb = mpy.ImageClip(thumbPath).set_duration(audio.duration)
sound = audio.to_soundarray()
fps = 24
sr = sound.shape[0]/audio.duration
img_raw = cv2.imread(thumbPath)
img_raw = cv2.resize(img_raw, (400, 400))

def get_sound(t):
  length = 255
  end = sr * t
  start = end - (sr/fps)
  start = 0 if start<0 else start
  L = sound[int(start):int(end), 0]
  # ax.set_xscale('log')
  ax.set_ylim(0, 10)
  hasil = np.fft.fft(L, length)
  freqs = np.fft.fftfreq(length)
  return abs(hasil[:length//2])

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
from moviepy.video.io.bindings import mplfig_to_npimage
# fig.set_dpi()
def generator(t):
  # img = img_raw.copy()
  # spectrum = igmov.analizer.Octave(get_sound(t))
  ax.clear()
  x = get_sound(t)
  ax.semilogx(x[4:])
  # ax.set_ylim(0, 200)
  # x, y = spectrum.get_result()
  # ax.plot(x[:21], y[:21])
  img = mplfig_to_npimage(fig)
  # temp_sound = get_sound(t)
  # norm = int(np.average(np.abs(temp_sound)) * 200 / np.max(temp_sound))
  # # norm = temp_sound.shape
  # img = cv2.line(img, (0, 50), (norm, 50), (255, 255, 255))


  # font = cv2.FONT_HERSHEY_SIMPLEX 
  # img = cv2.putText(img, str(norm), (50, 50), font, 1, (255, 54, 2))
  return img

video = mpy.VideoClip(
          generator, 
          duration=audio.duration,
          )
video.audio = audio
video.write_videofile('../sample/result.mp4', fps=fps)
# clip = mpy.CompositeVideoClip([video])
# clip.write_videofile('result.mp4', fps=fps)

# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
fig.set_dpi(10)
# %%
generator(5)

# %%
fig, ax = plt.subplots(1)
fig.set_dpi(100)
def get_signal(t):
  fourier = np.fft.rfft(np.concatenate([get_sound(t)]))
  freqs = np.fft.fftfreq(fourier.shape[0])
  ax.clear()
  ax.plot(abs(freqs) * (sound.shape[0]/audio.duration) , abs(fourier))
  # ax.set_xlim(100, 12000)
  # ax.set_xscale('log')
  # ax.set_yscale('log')
  ax.set_ylim(0, 500)
  print(freqs.shape)
  return fig

get_signal(12)
plt.show()

# %%
freq_list = get_freq_list()
# %%
fourier = np.fft.rfft(get_sound(12))
freqs = np.fft.fftfreq(fourier.shape[0])