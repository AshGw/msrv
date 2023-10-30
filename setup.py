from setuptools import find_packages, setup

with open("scripts/requires.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="app",
    version="1.7.35",
    python_requires=">=3.10",
    packages=find_packages(exclude=["scripts", ".github", "tests"]),
    package_data={
        "app": ["**"],
    },
    exclude_package_data={
        "": [".gitignore", ".pre-commit-config.yaml", "README.md", ".env", ".flake8"],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
