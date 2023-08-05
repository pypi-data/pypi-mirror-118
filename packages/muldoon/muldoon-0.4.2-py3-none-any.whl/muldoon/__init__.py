"""A package for sifting meteorological data to look for and analyze vortex
encounters"""

__version__ = '0.4.2'
__author__ = 'Brian Jackson <bjackson@boisestate.edu>'
__all__ = ['met_timeseries', 'utils', 'read_data']

from .met_timeseries import *
from .utils import *
from .read_data import *
