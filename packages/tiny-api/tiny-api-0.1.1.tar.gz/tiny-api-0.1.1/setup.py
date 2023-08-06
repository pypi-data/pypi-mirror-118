from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()


NAME = "tiny-api"
DESCRIPTION = "A tiny web framework to create APIs rapidly"
URL = "https://github.com/kaushal-dhungel/tiny-api"
EMAIL = "kaushaldhungel01@gmail.com"
AUTHOR = "Kaushal Dhungel"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.1"

REQUIRED = [
    'WebOb==1.8.7',
    'PyJWT==2.1.0',
    'gunicorn==20.1.0',
    'parse==1.19.0',
    'Jinja2==3.0.1',
    'whitenoise==5.3.0',
    'python-dotenv==0.19.0',

]



setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    # long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    download_url = 'https://github.com/Kaushal-Dhungel/tiny-api/archive/refs/tags/0.1.1.tar.gz',
    packages=['tiny_api'],
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    keywords=['python api','tiny api','python backend api'],
    classifiers=[

        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
