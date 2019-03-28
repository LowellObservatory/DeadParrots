### Method

1. Create a master bias (zero) file by median combining all the darks (zeros).
2. Subtract this master bias from all of the flats.
3. Median combine the flats to create a master flat. (see methods.md for median combine)
4. Divide the master flat by its mean to get a normalized master flat.
5. For each data image, subtract the master bias and divide by the master flat.

### Questions
1. What about overscan pixels?
2. What if all the images are not the same size.
