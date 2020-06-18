# %%
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from moviepy.editor import *
import numpy as np

img = Image.open('../sample/result.jpg')
thumb = Image.open('../sample/result.logo.jpg')
splogo = Image.open('../igmov/assets/spotify_light.png').resize((100, 30), Image.ANTIALIAS)

# %%
logo = thumb.resize((170, 170), Image.ANTIALIAS).copy()
im = img.resize((400, 400), Image.ANTIALIAS).copy()
# %%
image = im.copy()
logo2 = logo.copy()
image = image.filter(ImageFilter.GaussianBlur(5))

yy = 85
# image.paste(logo2, (210, 30))
image.paste(splogo, (400 - 120, 400 - 50), splogo)
# image
mask = Image.new("RGBA", logo2.size)
endx, endy = mask.size
ImageDraw.Draw(mask).ellipse((5,5, endx - 5, endy - 5 ), fill="white")
image.paste(logo2, (115, 30 + yy), mask.filter(ImageFilter.GaussianBlur))
font = ImageFont.truetype('calibri.ttf', 20)
ImageDraw.Draw(image).multiline_text((20, 220 + yy), "010 Kangen Keluarga", font=font)
ImageDraw.Draw(image).line((20, 250 + yy, 120, 250 + yy), width=3)
# ImageDraw.Draw(image).ellipse((20, 300, 40, 320), width=1)
image
# %%
audio = AudioFileClip('../sample/sample.ogg')
# %%
fps = 24
sound = audio.to_soundarray()
sr = int(sound.shape[0] / audio.duration)
# %%

def get_sound(t):
  end = t * sr
  start = end - (sr / fps)
  return sound[int(start): int(end)]


def fft(data, n):
  data = np.fft.fft(data, 512)
  data = np.abs(data)
  x = np.array(range(1, len(data) + 1))
  x = np.log(x)
  xlog = np.linspace(np.min(x), np.max(x), n)
  return np.interp(xlog, x, data)


def drawCicrle(image, data):
  im = image.copy()
  x, y, r = 200, 200, 90
  for i, l in enumerate(data):
    x0 = x + r * np.sin(i * np.pi / len(data))
    x1 = x + (r + l) * np.sin(i * np.pi / len(data))
    y0 = y - r * np.cos(i * np.pi / len(data))
    y1 = y - (r + l) * np.cos(i * np.pi / len(data))
    ImageDraw.Draw(im).line((x0, y0, x1, y1))
  return im
  
def drawCicrleF(image, data):
  im = image.copy()
  x, y, r = 200, 200, 90
  for i, l in enumerate(data):
    x0 = x - r * np.sin(i * np.pi / len(data))
    x1 = x - (r + l) * np.sin(i * np.pi / len(data))
    y0 = y - r * np.cos(i * np.pi / len(data))
    y1 = y - (r + l) * np.cos(i * np.pi / len(data))
    ImageDraw.Draw(im).line((x0, y0, x1, y1))
  return im


def draw(image, data):
  im = image.copy()
  x, y = 20, 260 + yy
  for i, l in enumerate(data):
    tall = l
    xx = x + i * 4
    ImageDraw.Draw(im).line((xx, y + tall, xx, y))
  return im.resize((400, 400), Image.ANTIALIAS)


def generator(t):
  lagu = get_sound(t)
  L = lagu[:, 0]
  R = lagu[:, 1]
  fft_data = fft(L, (1080 - 40) // 4)
  fft_data2 = fft(L, 80)
  # im = draw(image, fft_data)
  im = drawCicrle(image, fft_data2)

  fft_data = fft(R, (1080 - 40) // 4)
  fft_data2 = fft(R, 80)
  im = drawCicrleF(im, fft_data2)
  return np.array(im)


# clip = VideoClip(generator, duration=audio.duration)
# clip.audio = audio
# clip.write_videofile('../sample/result.mp4', fps=fps)
Image.fromarray(generator(5))
  

