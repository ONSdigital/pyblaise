import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="pyblaise",
  version="0.0.1",
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
  python_requires='>=3.6',
  install_requires=["jinja2", "requests"],
  package_data={'pyblaise': ['templates/*.template', 'templates/survey/*.template']},
)