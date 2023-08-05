import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mingo",
    version="0.0.7",
    author="Nicholas M. Synovic",
    author_email="nicholas.synovic@gmail.com",
    description="A Python project to get a list of programming languages from Wikipedia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NicholasSynovic/mingo",
    project_urls={
        "Bug Tracker": "https://github.com/NicholasSynovic/mingo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=["bs4", "lxml", "requests"],
)
