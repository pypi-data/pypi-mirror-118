"""
ctpros is a tool developed to aid in the visualization of and imaging pipeline for micro-computed tomography and MR research.

ctpros is composed of 3 subpackages:

- graphics
  defines the GUI-side logic with heavy usage of tkinter
- img
  defines the API-side of image IO and processing
- protocol
  defines standardized scripts utilizing the API for predetermined batched operations
"""
import layz_import

modules = [
    "mayavi",
    "mayavi.mlab",
    "pandas",
    "scipy.linalg",
    "scipy.ndimage",
    "scipy.optimize",
    "scipy.stats",
    "scipy.signal",
    "skimage.feature",
    "skimage.filters" "skimage.measure",
    "skimage.morphology",
    "scipy",
    "skimage",
    "vtk",
]
for module in modules:
    layz_import.layz_module(module)

from .img import *
from .graphics import GUI
from .graphics import Updater
from . import protocols
