"""
Analyzer to generate fft spectrum
"""

def fft(signal, count=256):
  """FFT to get freq response with custom resolution
  :param signal: Array 1D, signal data
  :param count: integer, total result
  """
  import numpy
  length = int(count*2)
  signal = numpy.array(signal)
  result = numpy.fft.fft(signal, length)
  result = abs(result[:length//2])
  return result

def to_log(data, count=256):
  """Converter signal to log scale using interpolation
  :param data: Array 1D
  :param count: integer, total result lenght
  """
  import numpy as np
  spectrum = np.array(data)
  xlog = np.log(np.array(range(1, spectrum.shape[0]+1)))
  xnew = np.linspace(np.min(xlog), np.max(xlog), count)
  newspectrum = np.interp(xnew, xlog, spectrum)
  return newspectrum

def interpolate(data, count=256):
  import numpy as np
  spectrum = np.array(data)
  xlog = np.array(range(spectrum.shape[0]))
  xnew = np.linspace(np.min(xlog), np.max(xlog), count)
  newspectrum = np.interp(xnew, xlog, spectrum)
  return newspectrum

def get_sample(signal, t, sr=44100, fps=24):
  """Sample getter for analyzer fft.
  :param signal: array 1D, signal data
  :param t: number, time position of signal
  """
  end = sr * t
  start = end - (sr/fps)
  start = 0 if start < 0 else start
  result = signal[int(start):int(end)]
  return result

def spectrum(signal, is_log=True, count=256, fft_res=256):
  """Spectrume Generator"""
  import numpy as np
  data = fft(signal, count=fft_res)
  data = to_log(data, count) if is_log else interpolate(data, count)
  return data

def spectrum_sig(signal, t, is_log=True, sr=44100, fps=24, count=256, fft_res=256):
  """Get Spectruom of sample
  """
  data = get_sample(signal, t, sr, fps)
  return spectrum(data, is_log, count, fft_res)
