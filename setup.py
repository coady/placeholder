+from distutils.core import setup

setup(
    name='placeholder',
    version='0.3.1',
    description='Operator overloading for fast anonymous functions.',
    long_description=open('placeholder.py').read().split('"""\n')[1],
    author='Aric Coady',
    author_email='aric.coady@gmail.com',
    py_modules=['placeholder'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Python Software Foundation License',
    ],
)
