from setuptools import setup, find_packages

VERSION = 'v0.2-alpha.3'
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
        'astroid==2.5',
        'atomicwrites==1.4.0',
        'attrs==21.2.0',
        'build==0.6.0.post1',
        'certifi==2021.5.30',
        'chardet==4.0.0',
        'colorama==0.4.4',
        'flake8==3.8.4',
        'idna==2.10',
        'iniconfig==1.1.1',
        'isort==5.9.3',
        'lazy-object-proxy==1.6.0',
        'mccabe==0.6.1',
        'packaging==21.0',
        'pep517==0.11.0',
        'pluggy==0.13.1',
        'py==1.10.0',
        'pycodestyle==2.6.0',
        'pyflakes==2.2.0',
        'pylint==2.6.0',
        'pyparsing==2.4.7',
        'pytest==6.2.2',
        'requests==2.25.1',
        'toml==0.10.2',
        'tomli==1.2.1',
        'urllib3==1.26.6',
        'wrapt==1.12.1',
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
