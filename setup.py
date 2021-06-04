from setuptools import setup, Extension

setup(ext_modules=[Extension('placeholder.partials', ['placeholder/partials.c'])])
