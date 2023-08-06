"""
Package contain functions which are useful for operations at International System of Units SI units.

e.g.
print(units.compare__units('1/m', 'm**-1', 'm^-2*m', values=True))
"""

from .standardise_ import *
from .const import *
from .tools import *

