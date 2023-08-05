from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cleanlizard',
    version='0.1.3',
    author='Christopher Agard',
    author_email='cragard@gmail.com',
    description="Python library for cleaning CC lizard data",
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
