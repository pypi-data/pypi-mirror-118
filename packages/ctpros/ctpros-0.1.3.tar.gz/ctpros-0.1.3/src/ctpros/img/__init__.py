"""API subpackage of ctpros

This package defines the IO of various research image datatypes and image processing components.
"""
from .classes import *

supported_types = [
    ("Image", ["*.npy", "*.aim*", "*.jpg", ".mda"]),
]
