import setuptools
import os
import io

here = os.path.abspath(os.path.dirname(__file__))

DESCRIPTION = ""

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setuptools.setup(
    name="drf_nested",
    version="0.1.16",
    author="Andréas Kühne, Artur Veres",
    author_email="andreas.kuhne@promoteint.com, artur8118@gmail.com",
    maintainer="Artur Veres",
    maintainer_email="artur8118@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/promoteinternational/drf-nested",
    packages=setuptools.find_packages(exclude=["examples"]),
    install_requires=[
        'Django>=2.0',
        "djangorestframework>=3.8.0"
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
