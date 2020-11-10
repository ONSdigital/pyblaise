import setuptools
import subprocess

with open("README.md", "r") as fh:
    long_description = fh.read()

version = subprocess.check_output(["git", "describe"]).strip()

setuptools.setup(
    name="pyblaise",
    version=version,
    author="ed grundy",
    author_email="edward.grundy@ext.ons.gov.uk",
    description="A simple wrapper to the Blaise SOAP interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["jinja2", "requests", "requests_mock"],
    package_data={"pyblaise": ["templates/*.template", "templates/survey/*.template"]},
)
