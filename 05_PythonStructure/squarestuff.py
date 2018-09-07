"""
This module defines a function called 'square' and another called
'sum_of_squares'

It also has a 'main' function
"""

def square(x):
    """Square the input number and return it."""

    y = x * x
    return y

def sum_of_squares(x, y, z):
    """Calculate the sum of squares of three input numbers."""

    a = square(x)
    b = square(y)
    c = square(z)

    return a + b + c

def main():
    '''Test "sum_of_squares".'''

    a = -5
    b = 2
    c = 10
    result = sum_of_squares(a, b, c)
    print(result)
    
if __name__ == "__main__":
    main()
