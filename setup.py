from setuptools import setup, find_packages

setup(
    name="projman",
    version="1.0.0",
    description="Time Estimation and forecast Tool for Projects",
    author="Andreas Thielmann",
    packages=find_packages(),
    install_requires=[
        # Runtime dependencies
        'numpy>=2.3.5',
        'scipy>=1.17.0',
        'PyYAML>=6.0.3',
        'networkx>=3.6.1',
        'matplotlib>=3.7.0',
        'argparse>=1.4.0'
    ],
    entry_points={
        'console_scripts': [
            'projman=projman.__main__:main',
            'carlo=dependency_monte_carlo.__main__:main',
        ],
    },
    python_requires='>=3.8',
    include_package_data=True,
)
