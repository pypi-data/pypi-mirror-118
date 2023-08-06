from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

projectName = 'pyXhPomMgmt'
projectDescritpion = 'python maven pom info extractor'
version = "0.0.2"
modules = [projectName, "POMREPOS", "POM", "Dependency", "ScanDir"]
url = "https://github.com/xh-dev-py/pyXhPomMgmt"
author = "xethhung"
email = "pypi@xethh.dev"

setup(
    name=projectName,
    version=version,
    description=projectDescritpion,
    py_modules=modules,
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    author=author,
    author_email=email,
    entry_points={'console_scripts': ['Package = %s:main' % projectName], },
    extras_require={
        "dev": [
            "pytest>=3.7",
        ]
    }
)
