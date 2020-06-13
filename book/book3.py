

# %%
from moviepy.editor import *
from moviepy.video.io.bindings import mplfig_to_npimage
import numpy as np
import matplotlib.pyplot as plt
import librosa
from librosa.display import waveplot

# %%
audio = AudioFileClip('../sample/sample.ogg')
y, sr = librosa.load('../sample/sample.ogg')
fig, ax = plt.subplots(1)
waveplot(y, sr=sr, color='b', alpha=.25)
last_t = 0
tempgraph =  mplfig_to_npimage(fig)
def animate(t):
    global last_t
    global tempgraph

    temp_t = np.round(t * 2)/2.
    if t > 0 and temp_t !=last_t:
        last_t = temp_t
        for coll in ax.collections:
            ax.collections.remove(coll)
        y2, sr2 = librosa.load('../sample/sample.ogg', mono=False, duration=t)
        waveplot(y2, sr=sr2, color='b', alpha=.8)
        waveplot(y, sr=sr, color='b', alpha=.25)
        tempgraph = mplfig_to_npimage(fig)
    return tempgraph

animate1 = VideoClip(animate, duration=audio.duration)
animate1.write_videofile('../sample/result.mp4', fps=24)

# %%
plt.axis('off')
waveplot(y[sr*5:sr*6], sr=sr)
plt.show()
animate1 = VideoClip(lambda t: mplfig_to_npimage(fig), duration=2)
animate1.write_videofile('../sample/result.mp4', fps=24)