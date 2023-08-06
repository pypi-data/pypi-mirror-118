import setuptools


setuptools.setup(
    name="SubScan",
    version="10.0.0",
    author="Negative.py",
    description="Module used to find directories and sub-domains of websites",
    long_description="SubScan is a script and a Python module that is used to find directories and subdomains of a web site using word lists, scan the ports of a machine, retrieve the route of a request... SubFinder has two main functions one for listing directories of a website on Windows that does not have an anonymous mode and one for listing directories of a website on Linux that has an anonymous mode.",
    url="https://github.com/Negative-py/SubScan",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["stem", "colorama"],
    packages=["SubScan"],
    package_data={"": ["*.txt", "*.config"]},
    python_requires=">=3.6",
)