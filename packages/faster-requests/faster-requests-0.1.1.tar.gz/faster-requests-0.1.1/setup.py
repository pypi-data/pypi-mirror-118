from setuptools import setup, find_packages

version = "0.1.1"
description = "Faster requests for Python 3"
long_description = "Faster-Requests is a simple package to send fast requests with Python 3"

setup(
    name="faster-requests",
    version=version,
    author="Dropout",
    description=description,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=[
        "python",
        "requests",
        "fast requests",
        "faster requests"
    ],
    classifiers=[
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)