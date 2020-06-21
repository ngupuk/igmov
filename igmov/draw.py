def fullCicrle(pos, image, data):
  """
  Draw full cirlcle spectrum.
  :param pos: (x, y, r) - position and radius of the circle
  :param image: PIL.Image - image to draw
  :param data: 1D array - spectrum data
  """
  from PIL import ImageDraw
  import numpy as np
  im = image.copy()
  x, y, r = pos
  for i, l in enumerate(data):
    x0 = x + r * np.sin(i * 2 * np.pi / len(data))
    x1 = x + (r + l) * np.sin(i * 2 * np.pi / len(data))
    y0 = y - r * np.cos(i * 2 * np.pi / len(data))
    y1 = y - (r + l) * np.cos(i * 2 * np.pi / len(data))
    ImageDraw.Draw(im).line((x0, y0, x1, y1))
  return im


def halfCicrle(pos, image, data):
  """
  Draw half circle spectrum clockwise.
  :param pos: (x, y, r) - position and radius of the circle
  :param image: PIL.Image - image to draw
  :param data: 1D array - spectrum data
  """
  from PIL import ImageDraw
  import numpy as np
  im = image.copy()
  x, y, r = pos
  for i, l in enumerate(data):
    x0 = x + r * np.sin(i * np.pi / len(data))
    x1 = x + (r + l) * np.sin(i * np.pi / len(data))
    y0 = y - r * np.cos(i * np.pi / len(data))
    y1 = y - (r + l) * np.cos(i * np.pi / len(data))
    ImageDraw.Draw(im).line((x0, y0, x1, y1))
  return im


def halfCicrleF(pos, image, data):
  """
  Draw half circle spectrum conter clockwise.
  :param pos: (x, y, r) - position and radius of the circle
  :param image: PIL.Image - image to draw
  :param data: 1D array - spectrum data
  """
  from PIL import ImageDraw
  import numpy as np
  im = image.copy()
  x, y, r = pos
  for i, l in enumerate(data):
    x0 = x - r * np.sin(i * np.pi / len(data))
    x1 = x - (r + l) * np.sin(i * np.pi / len(data))
    y0 = y - r * np.cos(i * np.pi / len(data))
    y1 = y - (r + l) * np.cos(i * np.pi / len(data))
    ImageDraw.Draw(im).line((x0, y0, x1, y1))
  return im


def line(pos, image, data, scale=1, spacing=3, mode='dual'):
  """
  Draw spectrum bars.
  :param pos: (x, y) - position of spectrum on image
  :param image: PIL.image - image to draw
  :param data: 1D array - spectrum data
  :param scale: number - scaling of bar lenght
  :param spacing: int - spacing between bars
  :param mode: dual | bottom | up - direction of bars
  """
  from PIL import ImageDraw
  im = image.copy()
  x, y = pos
  for i, l in enumerate(data):
    tall = l * scale
    xx = x + i * spacing
    if mode == 'bottom':
      y1 = y + tall
      y2 = y
    elif mode == 'up':
      y1 = y
      y2 = y - tall
    else:
      y1 = y + tall
      y2 = y - tall
    ImageDraw.Draw(im).line((xx, y1, xx, y2))
  return im


def lineSpectrum(pos, image, data, width, scale=1, spacing=3, mode="dual"):
  """
  Draw sepectrum bars.
  :param pos: (x, y) - position of spectrum bars on image
  :param image: PIL.Image - image to draw
  :param data: 1D array - sound data
  :param width: int - widht of spectrum on image
  :param scale: number - scaling of bars length
  :param spacing: int - spacing between bars
  :param mode: dual | bottom | up - direction of bars
  """
  from . import analyzer as anl
  count = int(width // spacing)
  spectrum_data = anl.fft(data, count)
  return line(pos, image, spectrum_data, scale, spacing, mode)


def blackMask(image, alpha=.5):
  """
  Draw black mask on image.
  :param image: PIL.Image - image to draw
  :param alpha: float - black mask intensity (0 - 1)
  """
  from PIL import Image
  mask = Image.new('RGB', image.size)
  im = Image.blend(image, mask, alpha)
  return im


def progressBar(pos, image, width, percent):
  """
  Draw proggress bar.
  :param pos: (x, y) - position bars
  :param image: PIL.Image - image to draw
  :param width: int - widht progress bar
  :param percent: float - percentage of proggres (0 - 1)
  """
  from PIL import Image, ImageDraw
  image = image.copy()
  im = Image.new('RGBA', (width + 5, 15))
  gray = (255, 255, 255, 100)
  drw = ImageDraw.Draw(im)
  drw.rectangle((5, 0, width - 5, 10), fill=gray)
  drw.ellipse((0, 0, 10, 10), fill=gray)
  drw.ellipse((width - 10, 0, width, 10), fill=gray)
  drw.ellipse((2, 2, 8, 8), fill='white')
  drw.rectangle((5, 2, 5 + (width - 10) * percent, 8), fill='white')
  endPos = ((width - 10) * percent + 2, 2, (width - 10) * percent + 8, 8)
  drw.ellipse(endPos, fill='white')
  image.paste(im, pos, im)
  return image


def rectangleFillCrop(image):
  """
  Make image in rectangle shape using fill crop.
  :param image: PIL.Image - image source
  """
  image = image.copy()
  x, y = image.size
  n = min(image.size)
  x1 = 0 if x == n else (x - n) // 2
  y1 = 0 if y == n else (y - n) // 2
  image = image.crop((x1, y1, n + x1, n + y1))
  return image
