from setuptools import setup, find_packages

setup(
    name="utg900e",
    version="0.1.0",
    description="Библиотека управления генераторами сигналов серии UTG900E через SCPI (VISA)",
    author="Shagen Dorunts",
    packages=find_packages(),
    install_requires=[
        "pyvisa>=1.11.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
