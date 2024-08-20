# MIRcatPy

MIRcatPy is a Python package designed to interface with the MIRcat SDK.

## Warning

This package is provided "as-is" and may contain errors or bugs that could affect the stability of your system or cause unintended behavior. Users should proceed with caution and thoroughly test the package in a controlled environment before deploying it in production. The use of the MIRcat system involves handling high-power lasers, which can be hazardous. Ensure that all safety protocols are followed, and proper protective equipment is used to prevent injury. Always adhere to safety guidelines and parameter provided your vendor when working with laser systems. The developers and maintainers of MIRcatPy are not responsible for any damage or injury resulting from the use of this package.

## Installation

To install MIRcatPy, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/richtefee/MIRCatPy
   cd mircatpy
   ```
3. **Install Required Python Packages:**
   ```bash
   pip install .
   ```

4. **Install Required Libraries:**

   MIRcatPy requires additional DLL files to function correctly. These DLLs are not included in the repository. Please obtain the DLLs from Dalight Solutions or your vendor.

   The required DLLs are:

   - MIRcatSDK.dll

   To install the DLLs:

   - Place the DLLs in the Appropriate Directory:
     Place 32-bit DLLs in the mircatpy/libs/x32/ directory.
     Place 64-bit DLLs in the mircatpy/libs/x64/ directory.

   Example directory structure:
   ```
   mircatpy/
   ├── libs/
   │   ├── x32/
   │   │   └── MIRcatSDK.dll
   │   │   
   │   └── x64/
   │       └── MIRcatSDK.dll
   ```

## Usage

Once the package is installed and the required DLLs are in place, you can use the package in your Python scripts. Here’s a basic example:

```python
import time
from mircatpy import MIRcat

# Initialize the MIRcat instance
mc = MIRcat()

# Connect to the MIRcat laser system
mc.connect()

# Display the current status of the MIRcat system
mc.display_status()

# Enable laser emission
if not mc.check_laser_emission():
   mc.enable_emission()

# Get and display the current wavelength and wavenumber
wl, wn = mc.get_ww()

# Tune the laser to a specific wavelength
target_wavelength = 4.5  # microns
mc.tune("wl", target_wavelength)

# Start a sweep scan
start_wl = 4.0  # microns
end_wl = 5.0    # microns
scan_speed = 0.1  # microns per second
mc.StartSweepScan("wl", start_wl, end_wl, scan_speed, repetitions=2, bidirectional=True)
print(f"Started sweep scan from {start_wl} to {end_wl} microns.")

# Wait for a while to observe the scan (adjust time as needed)
time.sleep(10)

# Display scan status
print("Scan Status:")
mc.display_scanStatus()

# Stop the scan if it is still running
if mc.scanStatus["isScanInProgress"]:
   mc.stopScan()

# Disconnect from the MIRcat laser system
mc.disconnect()
```

## Citation
If you use MIRcatPy in your research or publications, please cite this package as follows:

Felix Richter, 2024. MIRcatPy: Python package for interfacing with the MIRcat SDK. [https://github.com/richtefee/MIRCatPy](https://github.com/richtefee/MIRCatPy).


## License

This project is licensed under a non commercial use license. See the LICENSE file for details.

## Contributing

If you would like to contribute to MIRcatPy, please fork the repository and submit a pull request with your changes.

## Support

For any issues or questions, please create an issue on the GitHub repository issues page.
