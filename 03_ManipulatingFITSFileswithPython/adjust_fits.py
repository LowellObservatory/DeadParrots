from astropy.io import fits
import numpy as np
from astropy.utils.data import get_pkg_data_filename
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style

image_file = get_pkg_data_filename('tutorials/FITS-images/HorseHead.fits')
hdul = fits.open(image_file)

plt.style.use(astropy_mpl_style)
image_data = hdul[0].data

fig1, (ax, ax2) = plt.subplots(2, 1, figsize=(8,8))

ax.imshow(image_data)
def onclick(event):
    print(int(round(event.xdata)))
    plot_data = image_data[:, int(round(event.xdata))]
    x = np.arange(len(plot_data))
    ax2.clear()
    ax2.plot(x, plot_data)
    fig1.canvas.draw_idle()
fig1.canvas.mpl_connect('button_press_event', onclick)
plot_data = image_data[100, :]
x = np.arange(len(plot_data))
ax2.plot(x, plot_data)
plt.show()
