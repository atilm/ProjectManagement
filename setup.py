from setuptools import setup, find_packages

setup(
    name="projman",
    version="1.0.0",
    description="Time Estimation and forecast Tool for Projects",
    author="Andreas Thielmann",
    packages=find_packages(),
    install_requires=[
        # Runtime dependencies
        'numpy>=1.23.0',
        'matplotlib>=3.7.0',
        'argparse>=1.4.0',
    ],
    entry_points={
        'console_scripts': [
            'projman=projman.__main__:main',
        ],
    },
    python_requires='>=3.8',
    include_package_data=True,
)
