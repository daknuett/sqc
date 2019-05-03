from setuptools import setup, find_packages

setup(
    name = "sqc",
    version = "0.0.1",
    packages = find_packages(),
    author = "Christoph Lehner",
    author_email = "",
    url = "https://github.com/lehner/sqc",
    install_requires = ["numpy"],
    description = "a simple digital quantum computer simulator",
    long_description = open("README.md").read(),
)
