import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ArPel-Controller", # Replace with your own username
    version="0.0.1",
    author="Sam Gustin",
    author_email="samwgustin@gmail.com",
    description="controls an array of multi-drectional plasma actuators",
    long_description="This package is an element of sam gustins masters thesis.  This package controls an array of multi-drectional plasma actuators",
    long_description_content_type="text/markdown",
    url="https://github.com/SWGustin/Thesis.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)