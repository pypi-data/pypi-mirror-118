import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maria",                     # This is the name of the package
    version="0.0.5",                 # The initial release version
    author="Thomas Morris",          # Full name of the author
    description='maria (Modeling Auto-Regressive Integrated Atmosphere)',
    url='https://github.com/tomachito/maria',
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    #packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',                   # Minimum version requirement of the package

    install_requires=['numpy',
                      'scipy',
                      'ephem',
                      'weathergen'],                     # Install other dependencies if any
    
    py_modules = ['tools','objects','tests'], 
    include_package_data=True,
    package_data={'': ['maria/site_info.csv']},
)
