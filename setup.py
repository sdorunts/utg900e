from setuptools import setup, find_packages

setup(
    name="utg900e",
    version="0.1.0",
    description="A Python library for controlling UTG900E series signal generators via SCPI commands using VISA interface",
    author="Shagen Dorunts",
    author_email="sdorunts@yandex.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pyvisa>=1.11.0",
        "colorlog>=6.9.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    project_urls={
        "Homepage": "https://github.com/sdorunts/utg900e",
        "Repository": "https://github.com/sdorunts/utg900e",
    },
)