from setuptools import setup, find_packages

with open ('Readme.md', 'r') as file:
    README = file.read()

setup(
    name="archean",
    version="1.1.0",
    description="Extract information from Wikipedia Dumps",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/thisisayushg/archean",
    author="Ayush Gupta",
    author_email="info@realpython.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["bs4", "requests", "mwparserfromhell", "pymongo"],
    entry_points={
        "console_scripts": [
            "archean=archean.__main__:main",
        ]
    },
)