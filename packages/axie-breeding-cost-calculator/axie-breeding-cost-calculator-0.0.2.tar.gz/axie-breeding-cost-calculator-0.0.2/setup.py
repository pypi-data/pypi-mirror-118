# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/



import setuptools
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="axie-breeding-cost-calculator",
    version="0.0.2",
    author="Florian Mitterbauer",
    description="Calculate how much SLP breeding cost will occur when pairing two Axies (Axie Infinity).",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/daflockinger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "axie_breeding_cost_calculator"},
    packages=setuptools.find_packages(where="axie_breeding_cost_calculator"),
    python_requires=">=3.6",
)