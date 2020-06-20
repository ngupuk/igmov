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

  _img = _pil.Image.new('RGB', (400, 400))
  _bg = _pil.Image.new('RGB', (400, 400))
  _logo = _pil.Image.new('RGB', (180, 180))
  _splogo = _pil.Image.new('RGBA', (100, 30))
  _title = ""
  _showSpotify = False

  def show(self):
    """
    Get PIL.Image of the first frame.
    """
    return self._gen()

  def _gen(self):
    bg = self._bg.copy()
    blur = self._imgfilter.GaussianBlur(3)
    bg = bg.filter(blur)
    mask = self._pil.Image.new('RGB', bg.size)
    bg = self._pil.Image.blend(bg, mask, .3)
    mask = self._pil.Image.new('RGBA', bg.size)
    self._imgdraw.Draw(mask).rectangle((105, 35, 310, 280), fill='black')
    mask = mask.filter(self._imgfilter.GaussianBlur(5))
    bg.paste(mask, (0, 0), mask)
    drw = self._imgdraw.Draw(bg)
    drw.rectangle((100, 30, 300, 270), fill='white')
    bg.paste(self._logo, (110, 40))
    font = self._imgfont.truetype('calibri.ttf', 13)
    drw.multiline_text((110, 230), self._title, font=font, fill="black")
    self._img = bg
    self._drawSpotify()
    return self._img

  def _drawSpotify(self):
    bg = self._img
    if self._showSpotify:
      font = self._imgfont.truetype('calibri.ttf', 12)
      self._imgdraw.Draw(bg).multiline_text((235, 370), "Listen On", font=font)
      bg.paste(self._splogo, (400 - 110, 400 - 40), self._splogo)
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
      pos = (100, 278)
      im2 = self._igmdraw.lineSpectrum(pos, im, sp_data, 200, mode='bottom')
      return self._np.array(im2)

    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True


class template2(template1):
  def _gen(self):
    bg = self._bg
    img = self._img
    logo = self._logo
    img.paste(bg, (0, 0))
    img = img.filter(self._imgfilter.GaussianBlur(3))
    img = self._igmdraw.blackMask(img, .5)
    mask = self._pil.Image.new('RGBA', logo.size)
    x, y = mask.size
    self._imgdraw.Draw(mask).ellipse((5, 5, x - 5, y - 5), fill="white")
    mask = mask.filter(self._imgfilter.GaussianBlur(3))
    logoX, logoY = logo.size
    img.paste(logo, (110, 80), mask)
    font = self._imgfont.truetype('calibri.ttf', 20)
    drw = self._imgdraw.Draw(img)
    drw.multiline_text((20, 320), self._title, font=font, fill="white")
    drw.line((20, 345, 90, 345), width=3)
    self._img = img
    self._drawSpotify()
    return self._img

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
      im = self._igmdraw.halfCicrle((200, 170, 95), im, Lfft)
      im = self._igmdraw.halfCicrleF((200, 170, 95), im, Rfft)
      return self._np.array(im)
    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True
