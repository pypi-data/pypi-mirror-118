from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="chocochip",
    version="0.0.1",
    author="Vignesh Baskaran",
    author_email="vignesh.sbaskaran@gmail.com",
    description="A package to provide you Chocochip cookies",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/VigneshBaskar/chocochip",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)