import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="declare",
    version="0.0.1",
    author="Chris Cardillo",
    author_email="cfcardillo23@gmail.com",
    description="Declarative Controller Interface for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chriscardillo/declare",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
