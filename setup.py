from distutils.core import setup, Extension

setup(
    name='placeholder',
    version='0.2.1',
    description='Operator overloading for fast anonymous functions.',
    long_description=open('__init__.py').read().split('"""\n')[1],
    author='Aric Coady',
    author_email='aric.coady@gmail.com',
    package_dir={'placeholder': ''},
    py_modules=['placeholder.__init__'],
    ext_modules=[Extension('placeholder.partial', ['partial.c'])],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Python Software Foundation License',
    ],
)
