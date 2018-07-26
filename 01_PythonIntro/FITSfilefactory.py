# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on Thu Mar 8 15:23:31 GMT+7 2018
#
#  @author: rhamilton

from __future__ import division, print_function, absolute_import

import os
import time
import numpy as np
import astropy.io.fits as pyf


if __name__ == "__main__":
    nfiles = 100
    delay = 1
    fpath = '/home/rhamilton/Playground/junk/'

    naxis1 = 1024
    naxis2 = 1024

    for i in range(nfiles):
        print(i+1)
        data = np.random.rand(naxis1, naxis2)
        fname = fpath + "/junk%04d.fits" % (i)
        print(fname)
        try:
            pyf.writeto(fname, data)
        except OSError as err:
            os.makedirs(fpath, exist_ok=True)
            pyf.writeto(fname, data, overwrite=True)
            print(str(err))
        time.sleep(delay)
