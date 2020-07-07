class template1(object):
  import numpy as _np
  from moviepy.editor import VideoClip as _vc
  from moviepy.editor import VideoFileClip as _vidFileClip
  import igmov.analyzer as _anl
  import igmov.draw as _igmdraw
  import igmov.dl as _igmdl
  import PIL as _pil
  from PIL import ImageFilter as _imgfilter
  from PIL import ImageDraw as _imgdraw
  from PIL import ImageFont as _imgfont
  import os as _os
  import os.path as _path

  _img = _pil.Image.new('RGB', (800, 800))
  _bg = _pil.Image.new('RGB', _img.size)
  _logo = _pil.Image.new('RGB', (360, 360))
  _splogo = _pil.Image.new('RGBA', (120, 35))
  _title = ""
  _username = ""
  _igLogo = _pil.Image.new('RGBA', (35, 35))
  _showSpotify = False
  _fontName = 'calibri.ttf'
  _vidBG = _vc()
  _isVidBG = False

  if(not _path.exists('__temp__')):
    _os.makedirs('__temp__')

  def useVideoBG(self, path):
    self._vidBG = self._vidFileClip(path)
    self._isVidBG = True
    return self

  def _drawVidBG(self, t):
    if(self._isVidBG):
      now = t % self._vidBG.duration
      img = self._vidBG.get_frame(now)
      img = self._pil.Image.fromarray(img)
      img = self._igmdraw.rectangleFill(img, self._bg.size[0])
      self._bg = img
      self._gen()
    return self._img

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
    font = self._imgfont.truetype(self._fontName, 24)
    drw = self._imgdraw.Draw(self._img)
    drw.text((x, y), self._title, font=font, fill='black')

  def _drawIg(self):
    x, y = self._img.size
    y -= (self._igLogo.size[1] + 20)
    x = 20
    if(self._username):
      font = self._imgfont.truetype(self._fontName, 24)
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
      font = self._imgfont.truetype(self._fontName, 24)
      self._imgdraw.Draw(bg).multiline_text((x, y + 8), "Listen On", font=font)
      bg.paste(self._splogo, (x + 100, y), self._splogo)
    self._img = bg

  def setBg(self, path):
    """
    Set background image from local image file.
    :param path: string - path of the image source
    """
    bg = self._pil.Image.open(path)
    self._bg = self._igmdraw.rectangleFill(bg, self._bg.size[0])
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
    splogoPath = '__temp__/spotify_light.png'
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
    ngupukLogoPath = '__temp__/ngupuk.jpg'
    try:
      ngLogo = self._pil.Image.open(ngupukLogoPath)
    except:
      self._igmdl.ngupukLogo(ngupukLogoPath)
      ngLogo = self._pil.Image.open(ngupukLogoPath)
    ngLogo = ngLogo.resize(self._logo.size, self._pil.Image.ANTIALIAS)
    self._logo = ngLogo
    return self

  def useInstagramLogo(self, username='ngupuk.id'):
    igLogoPath = '__temp__/ig.png'
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

  def useRandomBg(self, keyword, always_new=False):
    """
    Use random backgroun from unsplash.
    :param keyword: string - keyword of the image
    """
    bgpath = "__temp__/bg_%s.jpg" % keyword
    if(always_new):
      self._igmdl.background(keyword, bgpath)
      bg = self._pil.Image.open(bgpath)
    else:
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
    sound, sr, fps, duration, audio = anl.getAudioData(audioPath)
    L, _ = anl.extract(sound)

    def generator(t):
      self._drawVidBG(t)
      im = self._img.copy()
      sp_data = anl.getSound(t, L, sr, fps)
      pos = (200, 560)
      im2 = self._igmdraw.lineSpectrum(pos, im, sp_data, 380, 2, 5, 'bottom')
      return self._np.array(im2)

    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True

  def setFont(self, name):
    self._fontName = name
    return self


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
    sound, sr, fps, duration, audio = self._anl.getAudioData(audioPath)
    L, R = self._anl.extract(sound)

    def generator(t):
      self._drawVidBG(t)
      img = self._img.copy()
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

class template3(template1):

  _fontName = 'Gabriola.ttf'
  _logo2 = False

  def _drawLogo(self):
    x, y = (50, 200)
    logo = self._logo.resize((250, 250), self._pil.Image.ANTIALIAS)
    mask = self._pil.Image.new('RGBA', logo.size)
    drw = self._imgdraw.Draw(mask)
    drw.ellipse((5, 5, mask.size[0] - 5, mask.size[1] - 5), fill="white")
    blur = self._imgfilter.GaussianBlur()
    mask = mask.filter(blur)
    self._img.paste(logo, (x, y), mask)
    if(self._logo2):
      pos = (x + 150, y + 150)
      n = (100, 100)
      mask = mask.resize(n)
      logo2 = self._logo2.resize(n, self._pil.Image.ANTIALIAS)
      self._img.paste(mask, pos, mask)
      self._img.paste(logo2, pos, mask)

  def _drawTitle(self):
    x, y = (330, 240)
    titles = self._title.split('\n')
    for i, title in enumerate(titles):
      fontSize = 65 - i * 30
      font = self._imgfont.truetype(self._fontName, fontSize)
      drw = self._imgdraw.Draw(self._img)
      drw.text((x, y + i * 60), title, 'white', font)

  def makeVideo(self, audioPath, resultPath):
    """
    Make video file
    :param audioPath: string - path of audio source.
    :param resultPath: string - path of video result.
    """
    self._gen()
    anl = self._anl
    sound, sr, fps, duration, audio = anl.getAudioData(audioPath)
    L, _ = anl.extract(sound)

    def generator(t):
      im = self._img.copy()
      sp_data = anl.getSound(t, L, sr, fps)
      pos = (40, 580)
      im2 = self._igmdraw.lineSpectrum(pos, im, sp_data, 720, 1.5, 5)
      im2 = self._igmdraw.progressBar((320, 380), im2, 350, t/duration)
      font = self._imgfont.truetype(self._fontName, 30)
      drw = self._imgdraw.Draw(im2)
      drw.text((650, 350), "%02i:%02i" % (t//60, t % 60),'white', font)
      return self._np.array(im2)

    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True

class template4(template1):

  _fontName = template3._fontName
  def _drawLogo(self):
    n = 150
    logo = self._logo.resize((n, n), self._pil.Image.ANTIALIAS)
    lx, ly = logo.size
    x, y, r = (self._img.size[0] // 2 - ly // 2, 50, 20)
    mask = self._pil.Image.new('RGBA', logo.size)
    drw = self._imgdraw.Draw(mask)
    drw.rectangle((r, 0, lx - r, ly), 'white')
    drw.rectangle((0, r, lx, ly - r), 'white')
    drw.ellipse((lx- 2*r,0, lx, r * 2), 'white')
    drw.ellipse((0, 0, r * 2, r * 2), 'white')
    drw.ellipse((0, ly - r * 2, r * 2, ly), 'white')
    drw.ellipse((lx - r * 2, ly - r * 2, *logo.size), 'white')
    self._img.paste(logo, (x, y), mask)

  def _drawBg(self):
    blur = self._imgfilter.GaussianBlur(10)
    img = self._bg.filter(blur)
    self._img.paste(img, (0, 0))
    self._img = self._igmdraw.blackMask(self._img, .3)

  def _drawTitle(self):
    y = 300
    drw = self._imgdraw.Draw(self._img)
    W, H = self._img.size
    msgs = self._title.split("\n")
    HH = 0
    for i, msg in enumerate(msgs):
      font = self._imgfont.truetype(self._fontName, 50 + i * 100)
      w, h = drw.textsize(msg, font)
      drw.text(((W-w)//2, (HH + y)), msg, 'white', font, align='center')
      HH += h
    return self

  def makeVideo(self, audioPath, resultPath):
    """
    Make video file
    :param audioPath: string - path of audio source.
    :param resultPath: string - path of video result.
    """
    self._gen()
    anl = self._anl
    sound, sr, fps, duration, audio = anl.getAudioData(audioPath)
    L, R = anl.extract(sound)

    def generator(t):
      self._drawVidBG(t)
      im = self._img.copy()
      y = 125
      sp_data = anl.getSound(t, L, sr, fps)
      sp_data2 = anl.getSound(t, R, sr, fps)
      data = anl.fft(sp_data, 200//5)
      data2 = anl.fft(sp_data2, 200//5)
      pos = (self._img.size[0] // 2 + 80, y)
      pos2 = (self._img.size[0] // 2 - 80 - 200, y)
      im2 = self._igmdraw.line(pos, im, data, 1.5, 5)
      im2 = self._igmdraw.line(pos2, im2, data2[::-1], 1.5, 5)
      return self._np.array(im2)

    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True
