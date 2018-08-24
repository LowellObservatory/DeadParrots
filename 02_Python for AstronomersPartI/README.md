Python for Astronomers - Part I
===============================

*Given by Michael Mommert at Lowell Observatory on 2018 08 10.*

In the presentation, Michael did things interactively using the two sample data files here.
I took some notes on what he presented but I'm sure I didn't capture everything.

## Topics Covered
* lists
* Showing data types
* Introduce numpy arrays
* Array vs. list operations
* Using numpy.genfromtxt
* Slicing basics (introduce ":" operator)
* numpy.genfromtxt with names (introduce associative/record array concepts)
* More about datatypes (lists vs. numpy arrays)
* Introduce astropy
* Starting with astropy.table.Table
* Astropy Table.read (and point out that names come from comments on first line)
* Introduce matplotlib.pyplot
    * Point out that always need to plt.show()
    * Labels
* Introduce python functions
    * Point out return value of a function is the end
* Example of how to read the documentation (of scipy)
    * Used curve_fit in scipy.optimize 
    * Returned both answers as one value to show return typing
    * Used explicit variables as return afterwards
* plt.plot to put fit result over scatter data
* Improve fitting by improve model function (started with x\*\*3, then went for full polynomial)
* Explicit example of list expansion (pass \*popt to model function)

## Get Python
[Download Anaconda](https://www.anaconda.com/download/)

## Additional Links for More Detailed Overviews
Additional materials that should be reviewed for the basics like
datatypes and all that kind of stuff:

[Introduction to Astropy](https://github.com/astropy/astropy-workshops/tree/master/aas231_workshop)

[Introduction to Python for Scientists](https://github.com/mommermi/Introduction-to-Python-for-Scientists)