import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PatternOmatic",
    version="0.1.0",
    author="Miguel Revuelta Espinosa",
    author_email="revuel22@hotmail.com",
    description="AI/NLP (Spacy) Rule Based Matcher pattern finder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/revuel/PatternOmatic",
    packages=setuptools.find_packages(),
    scripts=['scripts/patternomatic.py'],
    install_requires=[
        'spacy==2.2.3',
        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz#egg=en_core_web_sm'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
