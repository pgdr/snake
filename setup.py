import os
import setuptools


def src(x):
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, x))


def _read_file(fname, op):
    with open(src(fname), "r") as fin:
        return op(fin.readlines())


def requirements():
    return _read_file("requirements.txt", lambda lines: "".join(lines))


setuptools.setup(
    name="snake",
    packages=["snake"],
    entry_points={"console_scripts": ["snake=snake:main"]},
    version="1.0",
    author="pgdr",
    license="MIT",
    install_requires=requirements(),
)
