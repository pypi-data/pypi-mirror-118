from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

projectName = 'pyXhWinClipTool'
projectDescritpion = 'python windows clip tools(calling native windows command'
version = "0.0.2"
modules = [projectName]
url = "https://github.com/xh-dev-py/pyXhWinClipTool"
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
