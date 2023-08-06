from setuptools import setup
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='sketchdraw',
    version='1.0.3',
    description='A simple Python Library to convert Real world images to pencil sketch',
    author= 'Bhavika Tambi',
    url = 'https://github.com/tambibhavika2000/sketch.git',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['sketch', 'pencil sketch', 'cartoonise'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['sketchdraw'],
    package_dir={'':'src'},
    install_requires = [
        'opencv-python'
    ]
)