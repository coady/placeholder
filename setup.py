from setuptools import setup, Extension

ext_module = Extension('placeholder.partials', ['placeholder/partials.c'], py_limited_api=True)
setup(ext_modules=[ext_module])
