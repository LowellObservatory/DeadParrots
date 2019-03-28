### To median combine a set of images in Python.

* Stack the 2d arrays to form a 3d array
* Compute the median using numpy.median passing axis=0 to compute along the dimension of stacking.

A simple example:

```python
>>> import numpy
>>> a = numpy.array([[1,2,3],[4,5,6]])
>>> b = numpy.array([[3,4,5],[6,7,8]])
>>> c = numpy.array([[9,10,11],[12,1,2]])
>>> d = numpy.array([a,b,c])
>>> d
array([[[ 1,  2,  3],
        [ 4,  5,  6]],

       [[ 3,  4,  5],
        [ 6,  7,  8]],

       [[ 9, 10, 11],
        [12,  1,  2]]])
>>> d.shape
(3, 2, 3)

>>> numpy.median(d, axis=0)
array([[ 3.,  4.,  5.],
       [ 6.,  5.,  6.]])
```
