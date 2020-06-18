class template1:
  import numpy as __np
  from moviepy.editor import VideoClip as __vc
  import igmov.analyzer as __anl
  import igmov.draw as __igmdraw
  import igmov.dl as __igmdl
  import PIL as __pil
  from PIL import ImageFilter as __imgfilter
  from PIL import ImageDraw as __imgdraw
  from PIL import ImageFont as __imgfont

  __img = __pil.Image.new('RGB', (400, 400))
  __bg = __pil.Image.new('RGB', (400, 400))
  __logo = __pil.Image.new('RGB', (180, 180))
  __splogo = __pil.Image.new('RGBA', (100, 30))
  __title = ""
  __showSpotify = False

  def show(self):
    return self.__gen()

  def __gen(self):
    bg = self.__bg.copy()
    blur = self.__imgfilter.GaussianBlur(3)
    bg = bg.filter(blur)
    mask = self.__pil.Image.new('RGB', bg.size)
    bg = self.__pil.Image.blend(bg, mask, .3)
    mask = self.__pil.Image.new('RGBA', bg.size)
    self.__imgdraw.Draw(mask).rectangle((105, 35, 310, 280), fill='black')
    mask = mask.filter(self.__imgfilter.GaussianBlur(5))
    bg.paste(mask, (0, 0), mask)
    drw = self.__imgdraw.Draw(bg)
    drw.rectangle((100, 30, 300, 270), fill='white')
    bg.paste(self.__logo, (110, 40))
    font = self.__imgfont.truetype('calibri.ttf', 13)
    drw.multiline_text((110, 230), self.__title, font=font, fill="black")
    if self.__showSpotify:
      self.__imgdraw.Draw(bg).multiline_text((235, 370), "Listen On", font=font)
      bg.paste(self.__splogo, (400 - 110, 400 - 40), self.__splogo)
    self.__img = bg
    return self.__img

  def setBg(self, path):
    bg = self.__pil.Image.open(path)
    self.__bg = bg.resize(self.__bg.size, self.__pil.Image.ANTIALIAS)
    return self

  def setTitle(self, text):
    self.__title = text
    return self

  def setLogo(self, path):
    logo = self.__pil.Image.open(path)
    self.__logo = logo.resize(self.__logo.size, self.__pil.Image.ANTIALIAS)
    return self

  def showSpotify(self):
    splogoPath = '__temp__.spotify_light.png'
    try:
      splogo = self.__pil.Image.open(splogoPath)
    except:
      self.__igmdl.spotifyLogoLight(splogoPath)
      splogo = self.__pil.Image.open(splogoPath)
    splogo = splogo.resize(self.__splogo.size, self.__pil.Image.ANTIALIAS)
    self.__splogo = splogo
    self.__showSpotify = True
    return self

  def useNgupukLogo(self):
    ngupukLogoPath = '__temp__.ngupuk.jpg'
    try:
      ngLogo = self.__pil.Image.open(ngupukLogoPath)
    except:
      self.__igmdl.ngupukLogo(ngupukLogoPath)
      ngLogo = self.__pil.Image.open(ngupukLogoPath)
    ngLogo = ngLogo.resize(self.__logo.size, self.__pil.Image.ANTIALIAS)
    self.__logo = ngLogo
    return self

  def useRandomBg(self, keyword):
    bgpath = "__temp__.bg_%s.jpg" % keyword
    try:
      bg = self.__pil.Image.open(bgpath)
    except:
      self.__igmdl.background(keyword, bgpath)
      bg = self.__pil.Image.open(bgpath)
    bg = bg.resize(self.__bg.size, self.__pil.Image.ANTIALIAS)
    self.__bg = bg
    return self

  def makeVideo(self, audioPath, resultPath):
    self.__gen()
    anl = self.__anl
    im = self.__img.copy()
    sound, sr, fps, duration, audio = anl.getAudioData(audioPath)
    L, _ = anl.extract(sound)

    def generator(t):
      sp_data = anl.getSound(t, L, sr, fps)
      pos = (100, 278)
      im2 = self.__igmdraw.lineSpectrum(pos, im, sp_data, 200, mode='bottom')
      return self.__np.array(im2)

    clip = self.__vc(generator, duration=duration)
    clip.audio = audio
    clip.write_videofile(resultPath, fps=fps)
    return True
