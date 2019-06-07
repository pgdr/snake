import setuptools

setuptools.setup(
    name="snake",
    packages=["snake"],
    entry_points={console_scripts: ["snake=snake:main"]},
    version="1.0",
    author="pgdr",
    license="MIT",
)
