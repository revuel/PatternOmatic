""" Setup tools (build distribution) module

This file is part of PatternOmatic.

Copyright © 2020  Miguel Revuelta Espinosa

PatternOmatic is free software: you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PatternOmatic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PatternOmatic. If not, see <https://www.gnu.org/licenses/>.

"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PatternOmatic",
    version="0.2.3",
    author="Miguel Revuelta Espinosa",
    author_email="revuel22@hotmail.com",
    description="AI/NLP (Spacy) Rule Based Matcher pattern finder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/revuel/PatternOmatic",
    packages=setuptools.find_packages(),
    scripts=['scripts/patternomatic.py'],
    install_requires=[
        'spacy==2.3.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
