from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'simpleaicv'
LONG_DESCRIPTION = 'A package which is used for image identification and the speak and take the commands'

# Setting up
setup(
    name="simpleaicv",
    version=VERSION,
    author="Aum",
    author_email="aumdev01@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyautogui','SpeechRecognition','pyttsx3'],
    keywords=['speech recognition', 'image identification', 'image clicker', 'speaking jarvis', 'jarvis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)