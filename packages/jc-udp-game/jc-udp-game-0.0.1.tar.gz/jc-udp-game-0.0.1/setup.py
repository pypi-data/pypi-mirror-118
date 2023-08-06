import os

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="jc-udp-game",
    version="0.0.1",
    author="JenCat",
    author_email="jencat@jencat.pro",
    description="Multiplayer UDP game",
    license="MIT",
    keywords="game pygame udp multiplayer",
    url='https://jencat.pro',
    packages=['src'],
    long_description='Multiplayer UDP game',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    entry_points=dict(
        console_scripts=[
            'jc-udp-game=src.main:run',
            'jc-udp-game-server=src.server:start'
        ]
    ),
    setup_requires=[
        'pygame'
    ]
)
