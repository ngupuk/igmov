# %%
import numpy as np
import moviepy.editor as mpy
import cv2
import igmov.analyzer as anl
import igmov.draw as drw

audioPath = '../sample/sample.ogg'
thumbPath = '../sample/thumb.jpg'

# %%
audio = mpy.AudioFileClip(audioPath)
thumb = mpy.ImageClip(thumbPath).set_duration(audio.duration)
sound = audio.to_soundarray()
fps = 24
sr = int(sound.shape[0]/audio.duration)
img_raw = cv2.imread(thumbPath)
img_raw = cv2.resize(img_raw, (400, 400))

# def interpolate(signal, count=100):
#   spectrum = signal
#   xlog = np.log(np.array(range(1, spectrum.shape[0]+1)))
#   xnew = np.linspace(np.min(xlog), np.max(xlog), count)
#   newspectrum = np.interp(xnew, xlog, spectrum)
#   return newspectrum

# def get_sound(t, length=255):
#   end = sr * t
#   start = end - (sr/fps)
#   start = 0 if start<0 else start
#   L = sound[int(start):int(end), 0]
#   # ax.set_xscale('log')
#   hasil = np.fft.fft(L, length)
#   freqs = np.fft.fftfreq(length)
#   return abs(hasil[:length//10])

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
from moviepy.video.io.bindings import mplfig_to_npimage
# fig.set_dpi()
from skimage.draw import line, circle
def generator(t):
  img = img_raw.copy()
  # img = np.zeros((400, 400, 3), np.uint8)
  # spectrum = igmov.analizer.Octave(get_sound(t))
  ax.clear()
  # ax.set_ylim(-10, 30)
  # x = get_sound(t)
  newX = anl.spectrum_sig(sound[:, 0], t, count=(400-40)//4)
  # newX = interpolate(x[:int(x.shape[0]/2)], 50)
  img = drw.spectrum(img, newX, 20, 300, spacing=4, factor=1.8)
  img = drw.spectrum(img, newX, 20, 320, spacing=4, factor=.3, direction='bottom')
  # for i, l in enumerate(newX):
  #   baseY = 350
  #   baseX = 20
  #   spacing = 7
  #   tall = int(l) if int(l) < 190 else 190
  #   xx, yy = line(baseY-tall, baseX + i*spacing, baseY+int(tall*.5), baseX+i*spacing)
  #   img[xx, yy] = [255, 255, tall]
  # ax.semilogx(x[4:])
  # plt.scatter(range(len(newX)), newX)
  # plt.scatter(range(len(newX)), -newX*.3)
  # for i, j in zip(range(len(newX)), newX):
  #   plt.plot([i, i], [-j*.3, j])
  # ax.set_ylim(0, 200)
  # x, y = spectrum.get_result()
  # ax.plot(x[:21], y[:21])
  # img = mplfig_to_npimage(fig)
  # temp_sound = get_sound(t)
  # norm = int(np.average(np.abs(temp_sound)) * 200 / np.max(temp_sound))
  # # norm = temp_sound.shape
  # img = cv2.line(img, (0, 50), (norm, 50), (255, 255, 255))


  # font = cv2.FONT_HERSHEY_SIMPLEX 
  # img = cv2.putText(img, str(norm), (50, 50), font, 1, (255, 54, 2))
  return img

# generator(5)
# plt.imshow(generator(10))
video = mpy.VideoClip(
          generator, 
          duration=audio.duration,
          )
video.audio = audio
video.write_videofile('../sample/result.mp4', fps=fps)
# clip = mpy.CompositeVideoClip([video])
# clip.write_videofile('result.mp4', fps=fps)

# %%
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(1)
# fig.set_dpi(10)
# # %%
# generator(5)

# # %%
# fig, ax = plt.subplots(1)
# fig.set_dpi(100)
# def get_signal(t):
#   fourier = np.fft.rfft(np.concatenate([get_sound(t)]))
#   freqs = np.fft.fftfreq(fourier.shape[0])
#   ax.clear()
#   ax.plot(abs(freqs) * (sound.shape[0]/audio.duration) , abs(fourier))
#   # ax.set_xlim(100, 12000)
#   # ax.set_xscale('log')
#   # ax.set_yscale('log')
#   ax.set_ylim(0, 500)
#   print(freqs.shape)
#   return fig

# get_signal(12)
# plt.show()

# # %%
# freq_list = get_freq_list()
# # %%
# fourier = np.fft.rfft(get_sound(12))
# freqs = np.fft.fftfreq(fourier.shape[0])