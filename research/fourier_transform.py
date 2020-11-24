import matplotlib.pyplot as plt
import numpy as np

dt = 0.01
t = np.arange(0, 10, dt)
y = np.cos(t)+np.cos(3*t)

plt.plot(t,y)
plt.show()