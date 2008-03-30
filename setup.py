import os, sys
from distutils import core, sysconfig, util

directory = 'build/lib.%s-%s' % (util.get_platform(), sys.version[:3])

core.setup(
    name='placeholder',
    version='0.1',
    description='Operator overloading for fast anonymous functions.',
    long_description='''
    A placeholder object uses operator overloading to create partially bound functions on-the-fly.
    When used in a binary expression, it will return a callable object with the other argument bound.
    It's useful for replacing lambda when doing functional programming.
    ''',
    author='Aric Coady',
    author_email='aric.coady@gmail.com',
    package_dir = {'placeholder': ''},
    py_modules=['placeholder.__init__'],
    ext_modules=[core.Extension('placeholder.partial', ['partial.c'])],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Python Software Foundation License',
    ],
)
