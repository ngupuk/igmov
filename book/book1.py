
# %% [markdown]
# MoviePy Testing
# Learn how to use `moviepy`

# %%
from moviepy.editor import *

audio = AudioFileClip('../sample/sample.ogg')
thumb = ImageClip('../sample/thumb.jpg')
video = ColorClip((400, 400), (0, 0, 0), duration=audio.duration)

resultPath = "../sample/result.mp4"

# %%
video = (video
            .set_fps(24)
            .set_duration(audio.duration)
            .set_audio(audio)
            )
thumb = (thumb
            .set_fps(24)
            .set_duration(audio.duration)
            .resize((video.w, video.h))
            )
videos = CompositeVideoClip([video, thumb])
videos.to_videofile(resultPath)

# %%

# Generate random bg from book-2.ipynb
bgPath = '../sample/result.jpg'
bg = (ImageClip(bgPath)
        .subclip((400,400))
        .resize((400, 400))
        .set_fps(24)
        .set_duration(audio.duration)
        )
logo = (thumb
        .resize((180, 180))
        .margin(20, opacity=0)
        )
bg.to_videofile(resultPath)
bg.ipython_display()

videos = CompositeVideoClip([video, bg, logo])
videos.to_videofile(resultPath)