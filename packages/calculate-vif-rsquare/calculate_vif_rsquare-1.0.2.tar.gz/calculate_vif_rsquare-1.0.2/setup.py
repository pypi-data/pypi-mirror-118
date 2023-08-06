import pathlib
import numpy
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="calculate_vif_rsquare",
    version="1.0.2",
    description="This function will use to calculate VIF and adjusted rsquare within featue columns or indipendent variables.",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/neerajbafila/calculate_vif_rsquare",
    author="Neeraj Bafila",
    author_email="neerajbafila@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    # packages=["calculate_vif_rsquare"],
    python_requires=">=3.6",
    py_modules=['calculate_vif_rsquare'],
    package_dir = {'':'src'},
    include_package_data=True,
    install_requires=[
        'pandas',
        'statsmodels'
    ],
    # entry_points={
    #     "console_scripts": [
    #         "square=square.__main__:main",
    #     ]
    # },
)
