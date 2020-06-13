# %%
import numpy as np
import matplotlib.pyplot as plt
# %%
a = np.array(range(1,100))
a = np.log(a)
plt.scatter(a, np.zeros(a.shape))
y = np.linspace(0, np.max(a), 20)
plt.scatter(y, np.zeros(y.shape) + 1)
