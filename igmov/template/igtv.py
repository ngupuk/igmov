
class Igtv1():
  import PIL.Image as _Img
  import PIL.ImageFilter as _Filter
  import PIL.ImageFont as _Font
  import PIL.ImageDraw as _Draw
  import igmov.analyzer as _Anl
  import igmov.dl as _igmDL
  import igmov.draw as _igmDraw
  import numpy as _np
  from moviepy.editor import VideoClip as _vc

  _img = _Img.new('RGB', (600, 1080))
  _bg = _Img.new('RGB', _img.size)
  _logo = _Img.new('RGB', (180, 180))
  _title = ""

  def show(self):
    """
    Get PIL.Image of the first frame.
    """
    return self._gen()

  def setBg(self, path):
    im = self._Img.open(path)
    self._bg = im.resize(self._bg.size, self._Img.ANTIALIAS)
    return self

  def useRandomBg(self, keyword):
    path = '__temp__.bg_%s.jpg' % keyword
    try:
      im = self._Img.open(path)
    except:
      self._igmDL.background(keyword, path)
      im = self._Img.open(path)
    im = im.resize(self._bg.size, self._Img.ANTIALIAS)
    self._bg = im
    return self

  def __drawLogo(self, img):
    x, y = (img.size[0] // 2 - 100, 200)
    mask = self._Img.new('RGBA', img.size)
    drw = self._Draw.Draw(mask)
    drw.rectangle((x + 20, y + 20, x + 220, y + 250), fill='black')
    mask = mask.filter(self._Filter.GaussianBlur(30))
    img.paste(mask, (0, 0), mask)
    drw = self._Draw.Draw(img)
    drw.rectangle((x, y, x + 200, y + 230), fill='white')
    img.paste(self._logo, (x + 10, y + 10))
    return img

  def __drawTitle(self, img):
    x, y = (50, 500)
    font = self._Font.truetype('calibri.ttf', 30)
    drw = self._Draw.Draw(img)
    drw.text((x, y), self._title, font=font)
    drw.line((x, y + 50, x + 100, y + 50), 'white', 5)
    return img

  def _gen(self):
    bg = self._bg.copy()
    bg = bg.filter(self._Filter.GaussianBlur(3))
    bg = self._igmDraw.blackMask(bg)
    bg = self.__drawLogo(bg)
    bg = self.__drawTitle(bg)
    self._img = bg
    return self._img

  def setLogo(self, path):
    im = self._Img.open(path)
    self._logo = im.resize(self._logo.size, self._Img.ANTIALIAS)
    return self

  def useNgupukLogo(self):
    path = '__temp__.ngupuk.jpg'
    try:
      im = self._Img.open(path)
    except:
      self._igmDL.ngupukLogo(path)
      im = self._Img.open(path)
    im = im.resize(self._logo.size, self._Img.ANTIALIAS)
    self._logo = im
    return self

  def setTitle(self, text):
    self._title = text
    return self

  def makeVideo(self, audipath, resultPath):
    self._gen()
    sound, sr, fps, duration, audio = self._Anl.getAudioData(audipath)
    L, _ = self._Anl.extract(sound)

    def generator(t):
      im = self._img.copy()
      data = self._Anl.getSound(t, L, sr, fps)
      im = self._igmDraw.lineSpectrum((50, 800), im, data, 500)
      return self._np.array(im)

    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True
