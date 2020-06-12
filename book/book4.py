# %%
import numpy as np
import moviepy.editor as mpy
import cv2

audioPath = './sample/sample.ogg'
thumbPath = './sample/thumb.jpg'

# %%
audio = mpy.AudioFileClip(audioPath)
thumb = mpy.ImageClip(thumbPath).set_duration(audio.duration)
sound = audio.to_soundarray()
fps = 24
img_raw = cv2.imread(thumbPath)
img_raw = cv2.resize(img_raw, (400, 400))

def get_sound(t):
  factor = (sound.shape[0]/audio.duration)/fps 
  # start = ( t - (1/factor)) * factor
  # start = 0 if start < 0 else start
  end = t * factor
  end = (t + 1) * factor if t == 0 else end
  start = end - factor
  start = 0 if start < 0 else start
  temp_sound = sound[int(start):int(end),0]
  return temp_sound


from moviepy.video.io.bindings import mplfig_to_npimage
def generator(t):
  # img = img_raw.copy()
  img = mplfig_to_npimage(get_signal(t))
  # temp_sound = get_sound(t)
  # norm = int(np.average(np.abs(temp_sound)) * 200 / np.max(temp_sound))
  # # norm = temp_sound.shape
  # img = cv2.line(img, (0, 50), (norm, 50), (255, 255, 255))


  # font = cv2.FONT_HERSHEY_SIMPLEX 
  # img = cv2.putText(img, str(norm), (50, 50), font, 1, (255, 54, 2))
  return img

# video = mpy.VideoClip(
#           generator, 
#           duration=audio.duration,
#           )
# video.audio = audio
# clip = mpy.CompositeVideoClip([video])
# clip.write_videofile('result.mp4', fps=fps)

# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
fig.set_dpi(10)

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