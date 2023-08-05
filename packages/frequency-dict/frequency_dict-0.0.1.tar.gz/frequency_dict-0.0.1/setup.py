"""Setup for the frequency_dict package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Karthik Mandapaka",
    author_email="ravikarthik0802@gmail.com",
    name='frequency_dict',
    license="MIT",
    description='frequency_dict is a python package that helps with the finding the frequency of items in a '
                'collection easily.',
    version='v0.0.1',
    long_description=README,
    url='https://github.com/msvrk/frequency_dict',
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)