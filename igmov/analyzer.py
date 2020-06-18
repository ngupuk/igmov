def fft(data, n, res=512):
  import numpy as np
  data = np.fft.fft(data, res)
  data = np.abs(data)[:int(res * .8)]
  x = np.array(range(1, len(data) + 1))
  x = np.log(x)
  xlog = np.linspace(np.min(x), np.max(x), n)
  return np.interp(xlog, x, data)


def getSound(t, sound, sr=44100, fps=24):
  end = t * sr
  start = end - (sr / fps)
  return sound[int(start): int(end)]


def getAudioData(path):
  from moviepy.editor import AudioFileClip
  audio = AudioFileClip(path)
  fps = 24
  sound = audio.to_soundarray()
  sr = int(sound.shape[0] / audio.duration)
  return sound, sr, fps, audio.duration, audio


def extract(sound):
  L = sound[:, 0]
  R = sound[:, 1]
  return L, R
