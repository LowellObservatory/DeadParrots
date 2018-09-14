# ---------------------------- astropy.units
# http://docs.astropy.org/en/stable/units/

import astropy.units as u

# defining a quantity: a value with a unit
print(1*u.m)
print(type(1*u.m))

# or...
print(1*u.Unit('m'))
print(type(1*u.Unit('m')))

# units can be used as you would expect:

# you can form multiplicative units (in this case a velocity)
a = 1*u.m/u.s
print(a)

# # but you cannot add quantities with different units
# print(1*u.m + 2*u.s)

# units propagate properly through most astropy function and the basic
# numpy functions
import numpy as np
b = 2*u.m*u.m
print(b**2)
print(np.sqrt(b))

# in case the function cannot deal with units, you can strip the quantity
print(a.unit)
print(a.value)

# you can easily convert units
print(a.to(u.nm/u.yr))

# use equivalencies for mor complex transformations
# print((100*u.um).to(u.GHz)) # this does not work
print((100*u.um).to(u.GHz, equivalencies=u.spectral()))  # requires equiv.


# ------------------------------ astropy.table
# http://docs.astropy.org/en/stable/table/

from astropy.table import Table

# create a table
tab = Table([[1, 2, 3], [4, 5, 6], ['x', 'y', 'z']],
            names=('a', 'b', 'c'))

print(tab)

# easy to write to file
tab.write('table.dat', format='ascii')

# ... and to read from file
filetab = Table.read('table.dat', format='ascii')
print(filetab)


# accessing table content
print(tab['a'])
print(tab['a', 'c'])
print(tab['a', 'c'][1:3])
print(tab['a'] + tab['b'])
print(tab['a']**2)
# print(tab['a'] + tab['c'])

# modifying columns
tab['a'] = [10, 20, 30]
print(tab)

# adding columns
from astropy.table import Column
tab.add_column(Column(name='d', data=[1.1, 2.2, 3.3]))
print(tab)

# using units in tables
tab['a'].unit = u.m
tab['b'].unit = u.s
print(tab)
print(type(tab['a']))
print(tab['a']**2)  # wrong units!

# if using units in tables, use a QTable
from astropy.table import QTable
qtab = QTable(tab)
print(qtab)
print(type(qtab['a']))
print(qtab['a']/qtab['b'])  # correct units

# plotting table data
import matplotlib.pyplot as plt
plt.scatter(qtab['a'], qtab['b'])
plt.xlabel(qtab['a'].unit)
plt.ylabel(qtab['b'].unit)
# plt.show()

# and now for something completely different

# -------------------------------- astropy.visualization
# http://docs.astropy.org/en/stable/visualization/normalization.html

from astropy.io import fits
import matplotlib.pyplot as plt

hdu = fits.open('r20180617.060.fits')

# simple plotting has a useless range and stretch
plt.imshow(hdu[0].data, origin='lower')
# plt.show()

# using a manual stretch improves things
plt.imshow(hdu[0].data, origin='lower', vmin=1700, vmax=2000)
# plt.show()

# ... or better use astropy
from astropy.visualization import (ZScaleInterval, SquaredStretch,
                                   ImageNormalize)

norm = ImageNormalize(hdu[0].data,
                      interval=ZScaleInterval(), stretch=SquaredStretch())

plt.imshow(hdu[0].data, origin='lower', norm=norm)
plt.show()
