import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="drf_nested",
    version="0.1.0",
    author="Andréas Kühne, Artur Veres",
    author_email="andreas.kuhne@promoteint.com, artur8118@gmail.com",
    maintainer="Artur Veres",
    maintainer_email="artur8118@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/promoteinternational/drf-nested",
    packages=setuptools.find_packages(),
    install_requires=[
        'Django>=1.9.0',
        "djangorestframework>=3.5.0"
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
