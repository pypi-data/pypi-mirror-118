# @Author:  Felix Kramer
# @Date:   2021-05-23T23:25:28+02:00
# @Email:  kramer@mpi-cbg.de
# @Project: go-with-the-flow
# @Last modified by:    Felix Kramer
# @Last modified time: 2021-06-24T09:47:21+02:00
# @License: MIT



import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goflow", # Replace with your own username
    version="0.0.1",
    author="felixk1990",
    author_email="felixuwekramer@protonmail.com",
    description="Collecton of tools for computation of flows and and fluxes on Kirchhoff circuits and their corresponding adaptation. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felixk1990/go-with-the-flow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
