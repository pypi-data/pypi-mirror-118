import setuptools
from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as r:
    long_description = r.read()

setup(
    name="discord-economy",
    license='MIT',
    author='sldless',
    version='0.0.2',
    description="Make economy much easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['pymongo', 'py-cord'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

