def fft(data, n, res=512):
  """
  Get spectrum data in log scale using iterpolation.
  :param data: 1D array - sound data array
  :param n: int - total data result
  :param res: int - fft resolution before interpolation
  """
  import numpy as np
  data = np.fft.fft(data, res)
  data = np.abs(data)[:int(res * .8)]
  x = np.array(range(1, len(data) + 1))
  x = np.log(x)
  xlog = np.linspace(np.min(x), np.max(x), n)
  return np.interp(xlog, x, data)


def getSound(t, sound, sr=44100, fps=24):
  """
  Get part of the sound.
  :param t: float - time of the part
  :param sound: 1D array - sound data source
  :param sr: int - sample rate (total sample per second)
  :param fps: int - long of the sound part result is 1/fps
  """
  end = t * sr
  start = end - (sr / fps)
  return sound[int(start): int(end)]


def getAudioData(path):
  """
  Get audio data (sound, sr, fps, duration, andio)
  :param path: string - path of audio file source
  """
  from moviepy.editor import AudioFileClip
  audio = AudioFileClip(path)
  fps = 24
  sound = audio.to_soundarray()
  sr = int(sound.shape[0] / audio.duration)
  return sound, sr, fps, audio.duration, audio


def extract(sound):
  """
  Extract sound to L and R channel.
  :param sound: 2D array - sound with dual channel
  """
  L = sound[:, 0]
  R = sound[:, 1]
  return L, R
