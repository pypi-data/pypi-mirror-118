from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="rz-colorization",
    version="1.0.5",
    description="Rich Zhang's colorization model in the form of an easy to use python package.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arnavg115/colorization",
    author="Arnav G.",
    license="MIT",
    packages=["colorizers"],
    include_package_data=True,
    install_requires=["torch","scikit-image","numpy","matplotlib","Pillow"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)

