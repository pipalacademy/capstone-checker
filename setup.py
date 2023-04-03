from setuptools import setup, find_packages


setup(
    name="capstone-checker",
    version="0.1.0",
    description="Checker module for Capstone projects",
    author="Pipal Academy",
    url="https://github.com/pipalacademy/capstone-checker",
    packages=find_packages(),
    install_requires=[
        "requests==2.28.2",
        "pydantic==1.10.7",
        "PyYAML==6.0"
    ],
    entry_points={
        "console_scripts": [
            "capstone-checker = capstone_checker.__init__:main",
        ]
    }
)
