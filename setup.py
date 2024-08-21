from setuptools import setup, find_packages

setup(
    name="mircatpy",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["colorama"],
    package_data={
        "mircatpy": ["libs/x32/*", "libs/x64/*"],
    },
    entry_points={
        "console_scripts": [
            # Define any command-line scripts here
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Custom License",
        "Operating System :: OS Independent",
    ],
)
