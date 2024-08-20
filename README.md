# MIRcatPy

MIRcatPy is a Python package designed to interface with the MIRcat SDK. This package includes Python scripts and utilities for working with the MIRcat system.

## Citation
If you use MIRcatPy in your research or publications, please cite this package as follows:

Felix Richter, 2024. MIRcatPy: Python package for interfacing with the MIRcat SDK. [URL to GitHub repository]. DOI: [DOI]


## Installation

To install MIRcatPy, follow these steps:

1. **Clone the Repository:**

   git clone https://github.com/yourusername/mircatpy.git
   cd mircatpy

2. **Install Required Python Packages:**

   pip install .

3. **Install Required Libraries:**

   MIRcatPy requires additional DLL files to function correctly. These DLLs are not included in the repository. Please obtain the DLLs from Dalight Solutions or your vendor.

   The required DLLs are:

   - MIRcatSDK.dll

   To install the DLLs:

   - Place the DLLs in the Appropriate Directory:
     Place 32-bit DLLs in the mircatpy/libs/x32/ directory.
     Place 64-bit DLLs in the mircatpy/libs/x64/ directory.

   Example directory structure:

   mircatpy/
   ├── libs/
   │   ├── x32/
   │   │   └── MIRcatSDK.dll
   │   │   
   │   └── x64/
   │       └── MIRcatSDK.dll


## Usage

Once the package is installed and the required DLLs are in place, you can use the package in your Python scripts. Here’s a basic example:

import mircatpy

# Example usage of the MIRcatPy package

## Testing

To test the installation, make sure you have the required DLLs and run the unit tests provided in the tests directory:

pytest tests/

## License

This project is licensed under a non commercial use license. See the LICENSE file for details.

## Contributing

If you would like to contribute to MIRcatPy, please fork the repository and submit a pull request with your changes.

## Support

For any issues or questions, please create an issue on the GitHub repository issues page.
