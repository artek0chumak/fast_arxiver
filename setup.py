from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="fast_arxiver",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fast_arxiver=fast_arxiver:main.app",
        ],
    },
)
