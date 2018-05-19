from setuptools import setup

setup(
    name="onelinerizer",
    version="1.0.0",
    author="Chelsea Voss",
    author_email="csvoss@mit.edu",
    maintainer="Chelsea Voss and Anders Kaseorg",
    maintainer_email="onelinerizer@mit.edu",
    url='https://github.com/csvoss/onelinerizer',
    description='Convert any Python file into a single line of code.',
    packages=['onelinerizer'],
    entry_points={
        'console_scripts': ['onelinerizer=onelinerizer.__main__:main'],
    },
    test_suite='onelinerizer.runtests',
)
