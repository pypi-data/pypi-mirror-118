import os.path
from setuptools import setup


# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="agecal_mick",
    version="2.0.0",
    description="Compare age with mickzaa return older or younger",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mickzaa",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["agecal"],
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["realpython=agecal.__main__:main"]},
)