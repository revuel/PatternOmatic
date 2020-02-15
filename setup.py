import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PatternOmatic",
    version="0.1.0",
    author="Miguel Revuelta Espinosa",
    author_email="revuel22@hotmail.com",
    description="AI/NLP (Spacy) Rule Based Matcher pattern inder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/revuel/PatternOmatic",
    packages=setuptools.find_packages(),
    scripts=['scripts/patternomatic.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
