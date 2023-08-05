from . import version, constants, enums, functions

from .version import *
from .constants import *
from .enums import *
from .typedefs import *
from .functions import *
from .platform import *
from .exceptions import *

# from .experiment import *

__all__ = []
for subpackage in version, constants, enums, typedefs, functions, platform, exceptions:
    __all__ += subpackage.__all__

__version__ = version.PYOPENXR_VERSION  # Not in __all__, right?
