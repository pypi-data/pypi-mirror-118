"""
Setup and install the package.
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matlab2py",
    version="0.0.1",
    author="George Ebberson",
    author_email="george.ebberson@gmail.com",
    description="MATLAB-style figures for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GEbb4/matlab2py",
    project_urls={
        "Bug Tracker": "https://github.com/GEbb4/matlab2py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)