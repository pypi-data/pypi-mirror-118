## @package pyfrechet
#  Init file for package.

from ._strong_distance import lib as _sd

from ._weak_distance import lib as _wd

from .distance import Distance, StrongDistance, WeakDistance

from .optimise import BinarySearch

from .visualize import FreeSpaceDiagram
