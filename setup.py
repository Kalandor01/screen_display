from setuptools import setup, find_packages

from screen_display import __version__

setup(
    name='screen_display',
    version=__version__,

    url='https://github.com/Kalandor01/screen_display',
    author='Kalandor01',
    author_email='rohovszkyakoska@gmail.com',

    packages=find_packages(),
    
    install_requires=[
        'colorama',
    ],
)
