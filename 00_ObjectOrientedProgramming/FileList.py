
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
import glob
import os
from astropy.io import fits

class FileList(QListWidget):
    """ A widget containing a list of files and/or directories."""
    
    def __init__(self, image_display_figure):
        """ Point the filelist widget to a default directory and
            fill it with the contents of that directory.  Hook up
            a mouse double-click to call the 'item_click' method."""
            
        QListWidget.__init__(self)
        self.current_directory = "/data/lemi-archive-2016-04/*"
        self.add_items()
        self.image_display_figure = image_display_figure
        self.itemDoubleClicked.connect(self.item_click)

    def add_items(self):
        """Add items from the 'current_directory' to the list."""
        
        # Add the "up one directory" entry at the top of the list.
        item_text = ".."
        item = QListWidgetItem(item_text)
        self.addItem(item)
        
        # Add all the items in the directory to the list.
        # In this case, if the file is not a directory, it is a FITS file
        # so extract some header information to show with the file name.
        file_list = glob.glob(self.current_directory)
        for item_text in file_list:
            if (os.path.isfile(item_text) and (item_text.endswith("fits") or
                                               item_text.endswith("fit"))):
                # Catch errors in case this is not a FITS file or it
                # is a bad FITS file.
                try:
                    naxis1 = fits.getval(item_text, "NAXIS1")
                    naxis2 = fits.getval(item_text, "NAXIS2")
                    objname = fits.getval(item_text, "OBJNAME")
                    observer = fits.getval(item_text, "OBSERVER")
                    exptime = fits.getval(item_text, "EXPTIME")
                    try:
                        filters = fits.getval(item_text, "FILTERS")
                    except:
                        filters = "not defined"
                    item_text = (item_text + " (" + str(naxis1) + ','
                                 + str(naxis2) + ") " + objname + "  "
                                 + observer + "  " + str(exptime) +
                                 "  "  + str(filters))
                    item = QListWidgetItem(item_text)
                    self.addItem(item)
                except Exception as e:
                    print(str(e))
                    print(item_text)
                    print("error accessing FITS file or not a FITS file")
            else:
                item_text = item_text + "/"
                item = QListWidgetItem(item_text)
                self.addItem(item)

    def item_click(self, item):
        """ The user clicked on an item, decide what to do based on the item."""
        
        # Extract the path/file from the list item.
        dir_file = str(item.text())
        dir_file = (dir_file.split())[0]
        
        if (str(dir_file) == ".."):
            # Go up one directory.
            if (self.current_directory.endswith('*')):
                if(os.path.dirname(self.current_directory[:-2]) != "/"):
                    new_dir = os.path.dirname(self.current_directory[:-2]) + "/*"
                else:
                    new_dir = os.path.dirname(self.current_directory[:-2]) + "*"
            else:
                new_dir = os.path.dirname(self.current_directory) + "*"
            
            self.set_current_directory(new_dir)
            
        elif (os.path.isfile(str(dir_file))):
            # This is a file, so we read the image data and display.
            self.image_display_figure.update_image(dir_file)
        else:
            # They clicked on a directory, set current directory to that dir.
            self.set_current_directory(dir_file + "*")
            
    def set_current_directory(self, new_dir):
        """ Set the current directory to 'new_dir' and then reload the list."""

        self.current_directory = new_dir
        self.clear()
        self.add_items()
        self.update()
            