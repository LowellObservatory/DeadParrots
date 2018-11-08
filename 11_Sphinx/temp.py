def C_to_F(C):
    """Function to turn C into F

    :param C: Temperature in Celsius to be converted to Fahrenheit, float
    :return: Temperature in Fahrenheit, float
    :Example:

    >>> import temp
    >>> temp.c_to_f(16)
    60.8
    """
    return C*1.8+32


def F_to_C(F):
    """Function to turn F into C

    :param F: Temperature in Fahrenheit to be converted to Celsius, float
    :return: Temperature in Celsius, float
    :Example:

    >>> import temp
    >>> temp.f_to_c(16)
    16.11111
    """
    return (F-32)/1.8
