import numpy as np
from VisualizationCode import VisualizationCode as vc

x = np.arange (0,10,0.1)
y = np.cos(x)

vc.plot_line(x,y)
vc.plot_bar(x,y)