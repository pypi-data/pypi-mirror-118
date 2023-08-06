from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'API fetching to JSON'
LONG_DESCRIPTION = 'Automation of API fetching and converting to JSON (usually dicts), no hassle with clunky requests'

# Setting up
setup(
    name="apiget",
    version=VERSION,
    author="Al Razi",
    author_email="<abar.toha@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'API', 'apifetch', 'apiget', 'apicatch', 'apicall', 'apipull', 'api', 'json'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
