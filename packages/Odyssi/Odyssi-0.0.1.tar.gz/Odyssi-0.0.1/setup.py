from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Odyssi'

# Setting up
setup(
    name="Odyssi",
    version=VERSION,
    author="Polly",
    author_email="<dikshyamn327@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    
    packages=find_packages(),
    install_requires=[],
    keywords=['python','chatbot','oretes', 'programming for life'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)