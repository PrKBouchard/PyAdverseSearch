from setuptools import setup, find_packages

setup(
    name="PyAdverseSearch",
    version="1.0.0",
    description="Bibliothèque Python pour l'exploration de jeux adverses.",
    packages=find_packages(include=['PyAdverseSearch', 'PyAdverseSearch.*']),
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "arcade>=2.6.0",
        "reportlab"
    ],
)
