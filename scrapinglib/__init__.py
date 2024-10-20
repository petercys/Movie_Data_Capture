# -*- coding: utf-8 -*-

# This code adds the vendor directory to Python's path so it can find the modules
import os
import sys

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor/lib/python3.5/site-packages')
sys.path.append(vendor_dir)

from .api import search, getSupportedSources