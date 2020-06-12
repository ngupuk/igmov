# %%

import numpy as np

def get_freq_list():
  centerFrequency_Hz = np.array([39, 50, 63, 79, 99, 125, 157, 198, 250, 315, 
  397, 500, 630, 794, 1000, 1260, 1588, 2000, 2520, 3176, 4000, 5040, 6352, 8000, 10080, 
  12704, 16000])

  factor = np.power(10, 1.0/6.0)
  lowerCutoffFrequency_Hz=centerFrequency_Hz/factor;
  upperCutoffFrequency_Hz=centerFrequency_Hz*factor;

  return np.array(list(zip(lowerCutoffFrequency_Hz, upperCutoffFrequency_Hz)))
get_freq_list()