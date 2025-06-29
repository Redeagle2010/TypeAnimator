// setup.py
from setuptools import setup, find_packages

setup(
    name="typeanimator",
    version="0.1.0",
    author="Redeagle2010",
    description="Terminal Text Animation with color and speed",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/typeanimator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
