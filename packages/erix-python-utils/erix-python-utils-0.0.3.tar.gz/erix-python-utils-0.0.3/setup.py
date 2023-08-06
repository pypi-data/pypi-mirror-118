from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="erix-python-utils",
    version="0.0.3",
    author="Eric Stratigakis",
    author_email="enstrati@uwaterloo.ca",
    description="All of my utilities and tools in one place",
    py_modules=["homebrew"],
    package_dir={"":"src"},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["requests"],
    extra_requires={
        "dev":["pytest"]
    }
)