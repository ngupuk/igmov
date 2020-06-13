class Template1:
  """
    Ngupuk Template 1
    :param audio: string, path to audio string
  """
  def __init__(self, audio):
    import moviepy.editor as MP
    self.__MP = MP
    self.audio = self.__MP.AudioFileClip(audio)
    
