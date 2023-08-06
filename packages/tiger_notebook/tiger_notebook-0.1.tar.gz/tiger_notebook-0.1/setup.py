# -*- coding:utf-8 -*-
import os
from setuptools import find_packages
from setuptools import setup

install_requires = []
exclude_file_patterns = [".git"]
version = {}
with open(os.path.join("tiger_notebook/_version.py")) as fp:
    exec(fp.read(), version)
setup(
    name="tiger_notebook",
    version=version["__version__"],
    description="tiger notebook",
    url="",
    author="tiger",
    install_requires=install_requires,
    packages=find_packages(where=".", exclude=exclude_file_patterns),
    package_data={"": ["*.so"]},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tiger_component_drill=tiger_notebook.component_drill.__main__:main"
        ]
    }
)
