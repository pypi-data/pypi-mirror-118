import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="preprocessorAH",                    # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Anupam Hore",                     # Full name of the author
    author_email="anupam.hore@yahoo.com",
    description="preprocessorAH  Package for data pre-processing in Python",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    url="https://github.com/anupamhore/PythonDataPreprocessor.git",
    project_urls={
        "Bug Tracker": "https://github.com/anupamhore/PythonDataPreprocessor/issues",
    },
    packages=setuptools.find_packages(where="src"),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    package_dir={"":"src"},
    python_requires='>=3.8',                # Minimum version requirement of the package
    py_modules=["preprocessorAH"],             # Name of the python package
    install_requires=['statsmodels>=0.12.0','pandas>=0.25.3','scikit_learn>=0.24.2'] # Install other dependencies if any
)