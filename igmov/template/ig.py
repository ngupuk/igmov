class template1(object):
  import numpy as _np
  from moviepy.editor import VideoClip as _vc
  import igmov.analyzer as _anl
  import igmov.draw as _igmdraw
  import igmov.dl as _igmdl
  import PIL as _pil
  from PIL import ImageFilter as _imgfilter
  from PIL import ImageDraw as _imgdraw
  from PIL import ImageFont as _imgfont

  _img = _pil.Image.new('RGB', (800, 800))
  _bg = _pil.Image.new('RGB', _img.size)
  _logo = _pil.Image.new('RGB', (360, 360))
  _splogo = _pil.Image.new('RGBA', (125, 35))
  _title = ""
  _username = ""
  _igLogo = _pil.Image.new('RGBA', (35, 35))
  _showSpotify = False

  def show(self):
    """
    Get PIL.Image of the first frame.
    """
    return self._gen()

  def _drawBg(self):
    blur = self._imgfilter.GaussianBlur(3)
    img = self._bg.filter(blur)
    self._img.paste(img, (0, 0))
    self._img = self._igmdraw.blackMask(self._img)

  def _drawLogo(self):
    x, y = 200, 100
    logo = self._logo.copy()
    lx, ly = logo.size
    mask = self._pil.Image.new('RGBA', self._img.size)
    drw = self._imgdraw.Draw(mask)
    drw.rectangle((x + 40, y + 40, x + lx + 40, y + ly + 120), fill='black')
    blur = self._imgfilter.GaussianBlur(10)
    mask = mask.filter(blur)
    drw = self._imgdraw.Draw(mask)
    drw.rectangle((x, y, x + lx + 20, y + ly + 90), fill='white')
    mask.paste(logo, (x + 10, y + 10))
    self._img.paste(mask, (0, 0),  mask)

  def _drawTitle(self):
    x, y = 215, 480
    font = self._imgfont.truetype('calibri.ttf', 24)
    drw = self._imgdraw.Draw(self._img)
    drw.text((x, y), self._title, font=font, fill='black')

  def _drawIg(self):
    x, y = self._img.size
    y -= (self._igLogo.size[1] + 20)
    x = 20
    if(self._username):
      font = self._imgfont.truetype('calibri.ttf', 24)
      self._img.paste(self._igLogo, (x, y), self._igLogo)
      drw = self._imgdraw.Draw(self._img)
      drw.text((x + 40, y + 5), self._username, 'white', font)
    pass

  def _gen(self):
    self._drawBg()
    self._drawLogo()
    self._drawTitle()
    self._drawSpotify()
    self._drawIg()
    return self._img

  def _drawSpotify(self):
    x, y = self._img.size
    x -= self._splogo.size[0] + 120
    y -= self._splogo.size[1] + 20
    bg = self._img
    if self._showSpotify:
      font = self._imgfont.truetype('calibri.ttf', 24)
      self._imgdraw.Draw(bg).multiline_text((x, y + 8), "Listen On", font=font)
      bg.paste(self._splogo, (x + 100, y), self._splogo)
    self._img = bg

  def setBg(self, path):
    """
    Set background image from local image file.
    :param path: string - path of the image source
    """
    bg = self._pil.Image.open(path)
    self._bg = bg.resize(self._bg.size, self._pil.Image.ANTIALIAS)
    return self

  def setTitle(self, text):
    """
    Set video title.
    :param text: string - video title
    """
    self._title = text
    return self

  def setLogo(self, path):
    """
    Set logo from local storage.
    :param path: string - path of the logo source
    """
    logo = self._pil.Image.open(path)
    self._logo = logo.resize(self._logo.size, self._pil.Image.ANTIALIAS)
    return self

  def showSpotify(self):
    """
    Show Spotify's Logo on frame.
    """
    splogoPath = '__temp__.spotify_light.png'
    try:
      splogo = self._pil.Image.open(splogoPath)
    except:
      self._igmdl.spotifyLogoLight(splogoPath)
      splogo = self._pil.Image.open(splogoPath)
    splogo = splogo.resize(self._splogo.size, self._pil.Image.ANTIALIAS)
    self._splogo = splogo
    self._showSpotify = True
    return self

  def useNgupukLogo(self):
    """
    Use Ngupuk's logo. Automatic download from internet.
    """
    ngupukLogoPath = '__temp__.ngupuk.jpg'
    try:
      ngLogo = self._pil.Image.open(ngupukLogoPath)
    except:
      self._igmdl.ngupukLogo(ngupukLogoPath)
      ngLogo = self._pil.Image.open(ngupukLogoPath)
    ngLogo = ngLogo.resize(self._logo.size, self._pil.Image.ANTIALIAS)
    self._logo = ngLogo
    return self

  def useInstagramLogo(self, username='ngupuk.id'):
    igLogoPath = '__temp__.ig.png'
    try:
      igLogo = self._pil.Image.open(igLogoPath)
    except:
      url = 'https://ngupuk.github.io/static/instagram.png'
      self._igmdl.getFile(url, igLogoPath)
      igLogo = self._pil.Image.open(igLogoPath)
    igLogo = igLogo.resize(self._igLogo.size, self._pil.Image.ANTIALIAS)
    self._username = username
    self._igLogo = igLogo.convert('RGBA')
    return self

  def useRandomBg(self, keyword):
    """
    Use random backgroun from unsplash.
    :param keyword: string - keyword of the image
    """
    bgpath = "__temp__.bg_%s.jpg" % keyword
    try:
      bg = self._pil.Image.open(bgpath)
    except:
      self._igmdl.background(keyword, bgpath)
      bg = self._pil.Image.open(bgpath)
    bg = bg.resize(self._bg.size, self._pil.Image.ANTIALIAS)
    self._bg = bg
    return self

  def makeVideo(self, audioPath, resultPath):
    """
    Make video file
    :param audioPath: string - path of audio source.
    :param resultPath: string - path of video result.
    """
    self._gen()
    anl = self._anl
    im = self._img.copy()
    sound, sr, fps, duration, audio = anl.getAudioData(audioPath)
    L, _ = anl.extract(sound)

    def generator(t):
      sp_data = anl.getSound(t, L, sr, fps)
      pos = (200, 560)
      im2 = self._igmdraw.lineSpectrum(pos, im, sp_data, 380, 2, 5, 'bottom')
      return self._np.array(im2)

    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True


class template2(template1):

  def _drawLogo(self):
    x, y = self._img.size
    sx, sy = self._logo.size
    crop = 10
    x = (x - sx) // 2
    y = (y - sy) // 4
    mask = self._pil.Image.new("RGBA", self._logo.size)
    drw = self._imgdraw.Draw(mask)
    drw.ellipse((crop, crop, sx - crop, sy - crop), fill='white')
    blur = self._imgfilter.GaussianBlur(5)
    mask = mask.filter(blur)
    self._img.paste(self._logo, (x, y), mask)

  def _drawTitle(self):
    x, y = (30, 550)
    font = self._imgfont.truetype('calibri.ttf', 40)
    drw = self._imgdraw.Draw(self._img)
    drw.text((x, y), self._title, 'white', font)
    drw.line((x, y + 50, x + 100, y + 50), 'white', 5)

  def makeVideo(self, audioPath, resultPath):
    """
    Make video file
    :param audioPath: string - path of audio source.
    :param resultPath: string - path of video result.
    """
    self._gen()
    img = self._img.copy()
    sound, sr, fps, duration, audio = self._anl.getAudioData(audioPath)
    L, R = self._anl.extract(sound)

    def generator(t):
      Ldata = self._anl.getSound(t, L, sr, fps)
      Rdata = self._anl.getSound(t, R, sr, fps)
      Lfft = self._anl.fft(Ldata, 100)
      Rfft = self._anl.fft(Rdata, 100)
      im = img
      im = self._igmdraw.halfCicrle((400, 290, 180), im, Lfft * 2)
      im = self._igmdraw.halfCicrleF((400, 290, 180), im, Rfft * 2)
      return self._np.array(im)

    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True
