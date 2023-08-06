def foo(x, y, z):
    r"""
    This function uses a google-style docstring. In order for this documentation
    to render the way we want, we need to use the napolean sphinx extension.

    We can also use directives inside of the docstring, just like if this were 
    a .rst file.

    For example, euler's identity:
    .. math::

        e^{i \pi} + 1 = 0

    Args:
        x (int): description of x
        y (int): description of y
        z (int): description of z. blah blah blah blah blah
            another line of documentation for z

    Returns:
        x+y+z
    """
    return x + y + z

def bar(x):
    """Another function to document; will generate a page when linked to from autosummary

    Args:
        x (int)
    """
    return x

class Customer:
    """Customer class

    Args:
        name (str): customer's name
        phone_number (int): customer's phone number
    """
    def __init__(self, name, phone_number):
        self.name = name #: this is a docstring for a class attribute!
        self.number = phone_number

    def change_name_to_harry(self):
        """Legally change the customer's name to harry"""
        self._privately_change_name_to_harry()

    def _privately_change_name_to_harry(self):
        """This function will not generate documentation"""
        self.name = 'harry'

    def __eq__(self, other):
        """This will also not generate documentation"""
        return False