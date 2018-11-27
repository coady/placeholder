from setuptools import setup
import placeholder

setup(
    name='placeholder',
    version=placeholder.__version__,
    description='Operator overloading for fast anonymous functions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aric Coady',
    author_email='aric.coady@gmail.com',
    url='https://github.com/coady/placeholder',
    license='Apache Software License',
    py_modules=['placeholder'],
    python_requires='>=2.7',
    tests_require=['pytest-cov', 'pytest-parametrized'],
    keywords='functional lambda scala underscore',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
