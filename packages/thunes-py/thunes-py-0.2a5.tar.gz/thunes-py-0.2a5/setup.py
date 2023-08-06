from setuptools import setup, find_packages

VERSION = 'v0.2-alpha.5'
DESCRIPTION = 'Thunes Python Lib'
LONG_DESCRIPTION = open('README.md').read()

setup(
    name='thunes-py',
    version=VERSION,
    author='Ilton Ingui',
    author_email='iltoningui@outlook.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://pypi.org/project/thunes/',
    install_requires=[
        'requests==2.25.1',
    ],
    tests_require=['pytest'],
    keywords=['thunes', 'api', 'online', 'payment'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
