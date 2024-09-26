from setuptools import setup, find_packages

setup(
    name="solana_fm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
    ],
    description="Module for work Solana FM API",
    author="Tsunami43",
    url="https://github.com/Tsunami43/solana-fm",
)
