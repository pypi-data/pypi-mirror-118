from setuptools import setup

import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="rz-color-lite",
    version="0.0.2",
    description="Rich Zhang's colorization caffe model in the form of an easy to use python package.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arnavg115/colorization",
    author="Arnav G.",
    license="MIT",
    packages=["colorizer_lite"],
    include_package_data=True,
    install_requires=["tqdm","opencv-python","numpy"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)