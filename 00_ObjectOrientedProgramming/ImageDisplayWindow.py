'''
Created on Jul 9, 2018

@author: dlytle
'''

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import\
    FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg
from matplotlib.figure import Figure
import os
from astropy.io import fits
from astropy.visualization import (MinMaxInterval, SqrtStretch,
                                   ImageNormalize)


class ImageDisplayWindow(FigureCanvas):
    """Image Display Window is a widget used to display the FITS images."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        
        # Set up the matplotlib figure.
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.gca = fig.gca()   # Get Current Axes
        
        # Put an image in the figure at startup.
        self.compute_initial_figure()

        # Initialize our parent object (FigureCanvas) with our figure.
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        # Allow for the widget to expand/contract with the main widget.
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class StaticImageDisplayWindow(ImageDisplayWindow):
    """This is a specific kind of ImageDisplayWindow."""
    
    def compute_initial_figure(self):
        """ Load the default image into the ImageDisplayWindow."""
        
        rootDirectory = os.path.dirname(__file__)
        img=mpimg.imread(os.path.join(rootDirectory,
                        './images/fitsbrowser.jpg'))
        
        self.gca.clear()
        self.gca.imshow(img)
        
    def update_image(self, fits_file):
        """ Update the image displayed in the ImageDisplayWindow."""
        
        try:
            image_data = fits.getdata(fits_file, ext=0)
            sz = image_data.shape
            
            # Crop 10% of image all the way around the edge.
            new_image_data = self.crop_center(image_data, int(sz[0]*0.8),
                                              int(sz[1]*0.8))
            
            # Normalize the image to the range [0.0, 1.0].
            norm = ImageNormalize(new_image_data, interval=MinMaxInterval(),
                          stretch=SqrtStretch())
            
            # Plot image with "prism" color map and norm defined above.
            self.gca.imshow(new_image_data, cmap='prism', norm=norm)
            self.draw()
        except:
            print("Error reading and displaying FITS file")
        
    
    def crop_center(self, img, cropy, cropx):
        """ Crop the input 2D array (img) to the size indicated by
            (cropx,cropy).  The center of the image stays at the center."""
            
        y,x = img.shape
        
        startx = x//2-(cropx//2)
        starty = y//2-(cropy//2)    
        
        return img[starty:starty+cropy,startx:startx+cropx]

