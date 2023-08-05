from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1'
DESCRIPTION = 'avi'
LONG_DESCRIPTION = 'This is a youtube video downloader'


setup(
    name="YoutubeGui",
    version=VERSION,
    author="Rahul Shah",
    author_email="rahul.shah102006@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pytube3','tkinter'],
    keywords=[ 'YoutubeGui', 'Youtube', 'Rahul'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)