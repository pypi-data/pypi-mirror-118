from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="CubicBezier",
    packages=find_packages(include=["CubicBezier"]),
    version="0.1.0",
    install_requires=[
        "matplotlib",
        "numpy",],
    description="Cubic Bezier curve library",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mathias Ooi",
    author_email="mathias.ho.ooi@gmail.com",
    license="MIT",
)