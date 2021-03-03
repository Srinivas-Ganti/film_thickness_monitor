from HLG103 import HLG1_USB
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
#@{}
hlg1 = HLG1_USB()
hlg1.set_zero()
time.sleep(1)



# Typical single acq time - 28.890013 - 30 us

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative distance here

# Format plot
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)


plt.legend()

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    measurement = float(hlg1.read_measurement())*-1     
    xs.append(i)
    ys.append(measurement)
    
    # Limit x and y lists to 20 items
    xs = xs[-100:-1]
    ys = ys[-100:-1]

    # Draw x and y lists
    ax.clear()
    ax.scatter(xs, ys, label="Measured thickness", alpha = 0.4)
    ax.plot(xs, ys, label="Measured thickness", alpha = 0.8)
    plt.autoscale(axis = "both")
    ax.set_ylabel('Thickness (um)')
    ax.set_xlabel('samples')
    ax.set_title('Thickness scan')    

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=0.01)
plt.show()

