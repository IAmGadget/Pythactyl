import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Pythactyl",
    version="2.18",
    description="Pterodactyl panel API wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/iamgadget/Pythactyl",
    author="IAmGadget",
    author_email="info@iamgadget.co.uk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Pythactyl"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
