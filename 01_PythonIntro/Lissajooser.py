# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on Tue Feb 21 10:54:06 2017
#
#  @author: rhamilton

"""This is a one line description of this file.

If you want to write more about it, it can go down here.
It can really be as many lines as you want, so long as it's between
the triple quotation marks.
"""

from __future__ import division, print_function, absolute_import

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm


def calcLissajous(a, b, c, vasrms, phase, duration):
    """Calculate a Lissajous curve given a, b, RMS velocity, phase, and dur.

    A Lissajous curve is  is the graph of a system of parametric equations

    x=A*sin(a*t + theta)     y=B*sin(b*t)

    Args:
        a (:obj:`float`)
            Amplitude (in arcsec) of the Lissajous in the X direction
        b (:obj:`float`)
            Amplitude (in arcsec) of the Lissajous in the Y direction
        vasrms (:obj:`float`)
            RMS velocity (in arcsec/sec) of the scan to be performed
        phase (:obj:`float`)
            Phase of the sin component of the Lissajous scan
        duration (:obj:`float`)
            Total time duration (in seconds) of the scan

    Returns:
        (a whole bunch of stuff I don't feel like typing out)
    """
    # Time increment in seconds
    dt = .001

    f = vasrms/(2.*np.pi*np.sqrt((a*a + b*b*c*c)/2.))
    wx = 2.*np.pi*f*c
    wy = 2.*np.pi*f

    # Number of time steps
    tmax = int(duration/dt)

    # Put the phase into radians rather than degrees
    theta = 2.*np.pi*phase/360.

    t = np.arange(tmax)
    y = a*np.sin(wy*t*dt + theta)
    x = b*np.sin(wx*t*dt)
    vy = a*wy*np.cos(wy*t*dt)
    vx = b*wx*np.cos(wx*t*dt + theta)
    v = np.sqrt(vx*vx + vy*vy)

    # NOTE: If there are this many return values, you're probably better off
    #   making a class to contain them and then returning that instead!
    return t, dt, y, x, vy, vx, wx, wy, v


def calcLissajousComp():
    """For benchmarking only
    """
    a = 250.
    b = 250.
    c = np.sqrt(2.)
    vasrms = 200.
    phase = 42.
    duration = 80.

    # Time increment in seconds
    dt = .001

    f = vasrms/(2.*np.pi*np.sqrt((a*a + b*b*c*c)/2.))
    wx = 2.*np.pi*f*c
    wy = 2.*np.pi*f

    # Number of time steps
    tmax = int(duration/dt)

    # Put the phase into radians rather than degrees
    theta = 2.*np.pi*phase/360.

    t = np.arange(tmax)
    y = a*np.sin(wy*t*dt + theta)
    x = b*np.sin(wx*t*dt)
    vy = a*wy*np.cos(wy*t*dt)
    vx = b*wx*np.cos(wx*t*dt + theta)
    v = np.sqrt(vx*vx + vy*vy)

    # NOTE: If there are this many return values, you're probably better off
    #   making a class to contain them and then returning that instead!
    return t, dt, y, x, vy, vx, wx, wy, v


def calcLissajousLooper():
    """For benchmarking only
    """
    a = 250.
    b = 250.
    c = np.sqrt(2.)
    vasrms = 200.
    phase = 42.
    duration = 80.

    # Time increment in seconds
    dt = .001

    f = vasrms/(2.*np.pi*np.sqrt((a*a + b*b*c*c)/2.))
    wx = 2.*np.pi*f*c
    wy = 2.*np.pi*f

    tmax = int(duration/dt)    # Number of time steps

    t = np.zeros(tmax)
    x = np.zeros(tmax)
    y = np.zeros(tmax)
    vx = np.zeros(tmax)
    vy = np.zeros(tmax)
    v = np.zeros(tmax)
    theta = 2.*np.pi*phase/360.
    for i in range(tmax):
        t[i] = i
        y[i] = a*np.sin(wy*i*dt + theta)
        x[i] = b*np.sin(wx*i*dt)
        vy[i] = a*wy*np.cos(wy*i*dt)
        vx[i] = b*wx*np.cos(wx*i*dt + theta)
        v[i] = np.sqrt(vx[i]*vx[i] + vy[i]*vy[i])

    return t, dt, y, x, vy, vx, wx, wy, v


def plotphase(a, b, c, vasrms, dpix, phase, duration,
              plots=False, quiet=False):

    t, dt, y, x, vy, vx, wx, wy, v = calcLissajous(a, b, c, vasrms,
                                                   phase, duration)

    # NOTE: Since we don't really use vy or vx, we can just throw them
    #   away at the return time by putting "_" in their positions like so:
    t, dt, y, x, _, _, wx, wy, v = calcLissajous(a, b, c, vasrms,
                                                 phase, duration)

    # # Use these if you want to input speed in pixels/s and amps in pixels
    # vprms = 44.44     # Nominal rms scanning speed in pixels/s
    # vasrms = vprms*dpix       # Nominal rms scanning speed in arcsec/s
    # a,b,c = 300.,300.,sqrt(2) # y amplitude, x amplitude, frequency ratio
    # asORpix = 'pixels/s'

    # # Use these if you want to input speed in "/s and amps in arcsec
    vprms = vasrms/dpix                 # Nominal rms scan speed in pixels/s
    asORpix = 'arcsec/s'

    figscale = 8.
    if plots is True:
        figx, figy = figscale*b/a, figscale
        plt.figure(figsize=(figx, figy))
        plt.title('Scan Path')
        if asORpix == 'arcsec/s':
            plt.xlabel('arcsec')
            plt.ylabel('arcsec')
        else:
            plt.xlabel('pixels')
            plt.ylabel('pixels')
        plt.plot(x, y, 'r')
        plt.show(block=True)
        plt.figure(figsize=(figscale, figscale/2.))
        plt.title('Scan Speed')
        plt.ylabel(asORpix)
        plt.xlabel('time in seconds x' + str(1./dt))
        plt.plot(t, v)
        plt.show(block=True)

    if quiet is False:
        print('vprms=', vprms, 'pixels/s')
        print('vasrms=', vasrms, 'arcsec/s')
        print('x frequency =', wx/2.*np.pi)
        print('y frequency =', wy/2.*np.pi)
        print('rms speed =', np.sqrt(np.mean(v*v)), asORpix)
        print('mean speed =', np.mean(v), asORpix)
        if asORpix == 'arcsec/s':
            print('max speed =', max(v), 'arcsec/s',)
            print(' or ', max(v)/dpix, 'pix/s')
            print('x dimension =', 2.*b, 'arcsec',)
            print('   y dimension =', 2.*a, 'arcsec')
            print('minimum time/pixel =', 1./max(v)*dpix, 's')
        else:
            print('max speed =', max(v)*dpix,)
            print('arcsec/s', ' or ', max(v), 'pix/s')
            print('x dimension =', 2.*b*dpix, 'arcsec',)
            print('   y dimension =', 2.*a*dpix, 'arcsec')
            print('minimum time/pixel =', 1./max(v), 's')

    return t, x, y


if __name__ == "__main__":
    # Hopefully clear enough names
    yamp = 250.
    xamp = 250.
    freq = np.sqrt(2.)
    # Nominal rms scan speed in arcsec/s
    vasrms = 200.

    phases = np.arange(0, 181, 1)
    # Band A = 2.57 arcsec/pixel
    # Band B = 4.02 arcsec/pixel (theoretically)
    # Band C = 4.02 arcsec/pixel
    # Band D = 6.93 arcsec/pixel
    # Band E = 9.43 arcsec/pixel
    dpix = 9.43
    duration = 80.
    bins = np.arange(xamp*-1, xamp, step=dpix)

    zs = []
    for phase in phases:
        t, x, y = plotphase(yamp, xamp, freq, vasrms, dpix,
                            phase, duration, quiet=True, plots=False)
        counts, xedges, yedges, Image = plt.hist2d(x, y, bins=bins)
        del Image

        zs.append(len(np.where(counts == 0)[0]))
#        print phase, zs[-1]

    zs = np.array(zs)
    plt.close('all')
    plt.plot(phases, zs)
    plt.xlim([0, 181])
    plt.xlabel("Phase (deg)")
    plt.ylabel("Number of blank pixels in scan")
    plt.show(block=True)

    sorts = np.argsort(zs)
    rephases = phases[sorts]
    bestp = rephases[:20]
    worstp = rephases[-20:]
    print("Best phases:", bestp)
    print("Worst phases:", worstp)

    print("Best/worst num. of empty pixels:", zs[sorts][0], "/", zs[sorts][-1])
    print("Numpix:", counts.size)

    t, x, y = plotphase(yamp, xamp, freq, vasrms, dpix,
                        phases[sorts][0], duration, quiet=True, plots=False)

    counts, xedges, yedges, Image = plt.hist2d(x, y, bins=bins,
                                               norm=PowerNorm(0.5))
    Image.set_clim(vmin=0.0, vmax=200)
    plt.tight_layout()
    cbar = plt.colorbar()
    plt.show(block=True)

    t, x, y = plotphase(yamp, xamp, freq, vasrms, dpix,
                        phases[sorts][-1], duration, quiet=True, plots=False)

    counts, xedges, yedges, Image = plt.hist2d(x, y, bins=bins,
                                               norm=PowerNorm(0.5))
    Image.set_clim(vmin=0.0, vmax=200)
    plt.tight_layout()
    cbar = plt.colorbar()
    plt.show(block=True)
