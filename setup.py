from setuptools import find_packages, setup

setup(
    name="projects",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)