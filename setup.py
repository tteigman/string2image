import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="string2image",
    version="0.0.1",
    author="Tani Teigman",
    author_email="tteigman@gmail.com",
    url="https://github.com/tteigman/string2image",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
