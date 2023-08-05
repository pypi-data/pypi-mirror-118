from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'jarvis_module1'
LONG_DESCRIPTION = 'my small attempt, to make jarvisAI assistant jarvis can send emails,open youtube,browse web for you etc '

# Setting up
setup(
    name="jarvis_module1",
    version=VERSION,
    author="Neil bhurke",
    author_email="neilpython11@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['jarvisAI', 'python', 'AI', 'python tutorial', 'Neil bhurke'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)