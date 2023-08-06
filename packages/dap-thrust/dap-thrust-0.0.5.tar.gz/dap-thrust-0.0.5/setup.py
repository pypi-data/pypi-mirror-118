#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("thrust/__init__.py") as fp:
    exec(fp.read(), version)

# Dependencies
deps = []
with open("requirements.txt") as fp:
    deps = fp.read().splitlines()
deps = [x.strip() for x in deps]
deps = [x for x in deps if x and not x.startswith('#')]

setuptools.setup(
    name="dap-thrust",
    version=version['__version__'],
    author="Vipin Sharma",
    author_email="sh.vipin@gmail.com",
    description="PYDAP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitvipin/thrust",
    install_requires=deps,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={
        'thrust.data': ['*']
        }
)
