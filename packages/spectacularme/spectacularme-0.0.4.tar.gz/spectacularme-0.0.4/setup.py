"""Setup for the spectacularme package."""

import setuptools


setuptools.setup(
    author="Nemo Panther",
    author_email="nemopanther@protonmail.com",
    name='spectacularme',
    license="MIT",
    description='No cheese here',
    version='v0.0.4',
    long_description='README',
    url='https://github.com',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)