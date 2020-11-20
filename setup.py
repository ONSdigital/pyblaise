import setuptools
import subprocess


with open("README.md", "r") as fh:
    long_description = fh.read()


def get_git_version():
    """
    get pep440 compatible version string from tag/commit
    requirements:
    + history must have a tag (do not do a shallow clone, make an initial tag, etc)
    + tag must have the pattern '[N!]N(.N)*[{a|b|rc}N][.postN][.devN]' (see link)
      + use a for alpha, b for beta, rc for release candidate
      + postN for hotfixes
      + devN for developer versions
    + the commit sha (+<sha> in pep440) is omitted from the version string

    refs:
      https://www.python.org/dev/peps/pep-0440/
    """
    v = (
        subprocess.check_output(["git", "describe", "--always"], encoding="UTF-8")
        .strip()
        .split("-")
    )

    if len(v) == 3:
        version = "%s.dev%s" % (v[0], v[1])  # tag, commits away, no current hash
    else:
        version = v[0]  # git tag only

    # FIXME: check the regex
    # if not pep440.is_canonical(version):
    #    raise Exception("version string is not pep440 compatible: '%s'" % version)

    return version


setuptools.setup(
    name="pyblaise",
    version=get_git_version(),
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
    package_data={"pyblaise": ["operations/templates/*.template", "operations/templates/survey/*.template"]},
)
