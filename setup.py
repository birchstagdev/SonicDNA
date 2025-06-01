from setuptools import setup, find_packages

setup(
    name="ToonGloomStudio",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PySide6",
        "torch",
        "torchaudio",
        "audioldm2"
    ],
    entry_points={
        "console_scripts": [
            "toongloom = main:main"
        ]
    },
    author="Your Name",
    description="SonicDNA and generative music app.",
    python_requires=">=3.10",
)
