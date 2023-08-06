from setuptools import setup
import os

VERSION = "0.2.11"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="mc_ssh",
    description="mc_ssh is now mccli",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=['mc_ssh'],
    include_package_data=True,
    entry_points = {
        "console_scripts": ["mccli = mc_ssh.mccli:main"]
    },
    classifiers=["Development Status :: 7 - Inactive"],
)

