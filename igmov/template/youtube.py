class Template1():
  import numpy as _np
  import PIL.Image as _pilImage
  import PIL.ImageDraw as _imgDraw
  import PIL.ImageFont as _imgFont
  import PIL.ImageFilter as _imgFilter
  from igmov import analyzer as _anl
  from igmov import draw as _drw
  from igmov import dl as _dl
  from moviepy.editor import VideoClip as _vc

  _img = _pilImage.new('RGB', (1080, 600))
  _title = ""
  _users = []
  _bg = _pilImage.new('RGB', _img.size)
  _logo = _pilImage.new('RGB', (180, 180))
  _splogo = _pilImage.new('RGB', (100, 30))
  _showSplogo = False

  def useRandomBg(self, keyword):
    bgPath = '__temp__.bg_%s.jpg' % keyword
    try:
      bg = self._pilImage.open(bgPath)
    except:
      self._dl.background(keyword, bgPath)
      bg = self._pilImage.open(bgPath)
    bg = bg.resize(self._bg.size, self._pilImage.ANTIALIAS)
    self._bg = bg
    return self

  def useNgupukLogo(self):
    logoPath = "__temp__.ngupuk.jpg"
    try:
      logo = self._pilImage.open(logoPath)
    except:
      self._dl.ngupukLogo(logoPath)
      logo = self._pilImage.open(logoPath)
    logo = logo.resize(self._logo.size, self._pilImage.ANTIALIAS)
    self._logo = logo
    return self

  def showSpotify(self):
    spPath = '__temp__.spotify_light.png'
    try:
      splogo = self._pilImage.open(spPath)
    except:
      self._dl.spotifyLogoLight(spPath)
      splogo = self._pilImage.open(spPath)
    splogo = splogo.resize(self._splogo.size, self._pilImage.ANTIALIAS)
    self._splogo = splogo
    self._showSplogo = True
    return self

  def _drawSplogo(self):
    if self._showSplogo:
      im = self._img
      font = self._imgFont.truetype('calibri.ttf', 14)
      drw = self._imgDraw.Draw(im)
      drw.text((1080 - 210, 600 - 60), "Listen on", font=font)
      im.paste(self._splogo, (1080 - 150, 600 - 70), self._splogo)
      self._img = im
    return

  def _gen(self):
    bg = self._bg.copy()
    bg = bg.filter(self._imgFilter.GaussianBlur(10))
    bg = self._drw.blackMask(bg)
    mask = self._pilImage.new("RGBA", bg.size)
    drw = self._imgDraw.Draw(mask)
    drw.rectangle((120, 120, 320, 350), fill='black')
    mask = mask.filter(self._imgFilter.GaussianBlur(10))
    drw = self._imgDraw.Draw(mask)
    drw.rectangle((100, 100, 300, 330), fill='white')
    bg.paste(mask, (0, 0), mask)
    bg.paste(self._logo, (110, 110))
    self._img = bg
    self._drawTitle()
    self._drawUsers()
    self._drawSplogo()
    return self._img

  def _drawUsers(self):
    x = 330
    y = 180
    for i, user in enumerate(self._users):
      sx, sy = user.size
      xx = x + i * (sx + 10)
      yy = y - sy
      mask = self._pilImage.new('RGBA', user.size)
      drw = self._imgDraw.Draw(mask)
      drw.ellipse((5, 5, sx - 5, sy - 5), fill='white')
      mask = mask.filter(self._imgFilter.GaussianBlur(2))
      self._img.paste(user, (xx, yy), mask)
    return self

  def _drawTitle(self):
    if self._title:
      font = self._imgFont.truetype('calibri.ttf', 40)
      drw = self._imgDraw.Draw(self._img)
      drw.text((330, 200), self._title, font=font)
      drw.line((330, 250, 450, 250), width=5)
    return self

  def setUsers(self, *path):
    self._users.clear()
    for item in path:
      im = self._pilImage.open(item)
      im = im.resize((70, 70), self._pilImage.ANTIALIAS)
      self._users.append(im)
    return self

  def setBg(self, path):
    bg = self._pilImage.open(path)
    self._bg = bg.resize(self._bg.size, self._pilImage.ANTIALIAS)
    return self

  def setTitle(self, text):
    self._title = text
    return self

  def setLogo(self, path):
    logo = self._pilImage.open(path)
    self._logo = logo.resize(self._logo.size, self._pilImage.ANTIALIAS)
    return self

  def makeVideo(self, audioPath, resultPath):
    self._gen()
    sound, sr, fps, duration, audio = self._anl.getAudioData(audioPath)
    L, _ = self._anl.extract(sound)
    font = self._imgFont.truetype('calibri.ttf', 14)

    def generator(t):
      time = (t // 60, t % 60)
      im = self._img.copy()
      drw = self._imgDraw.Draw(im)
      drw.text((890, 260), "%02i:%02i" % time, font=font)
      data = self._anl.getSound(t, L, sr, fps)
      im = self._drw.lineSpectrum(
          (330, 300),
          im,
          data,
          600,
          mode='bottom',
          scale=2,
          spacing=4)
      im = self._drw.progressBar((328, 280), im, 600, t / duration)
      return self._np.array(im)
    clip = self._vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True
