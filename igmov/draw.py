def fullCicrle(pos, image, data):
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
  from . import analyzer as anl
  count = int(width // spacing)
  spectrum_data = anl.fft(data, count)
  return line(pos, image, spectrum_data, scale, spacing, mode)


def blackMask(image, alpha=.5):
  from PIL import Image
  mask = Image.new('RGB', image.size)
  im = Image.blend(image, mask, alpha)
  return im
