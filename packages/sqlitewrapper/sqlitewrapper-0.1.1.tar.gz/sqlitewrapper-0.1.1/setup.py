from setuptools import setup

with open("temp/README.md", "r") as file:
    description = file.read()

setup(
    name="sqlitewrapper",
    version="0.1.1",
    description="A python object-oriented wrapper for sqlite",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/judev1/sqlitewrapper",
    author="Jude",
    author_email="jude.cowden@protonmail.com",
    license="MIT",
    packages=["sqlitewrapper"],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)