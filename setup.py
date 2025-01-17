import io
import os
import re
import sys

from setuptools import setup, find_packages

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
with open("src/pygetwindow/__init__.py", "r") as fileObj:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
    ).group(1)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

requirements = ['pyrect==0.2.0', 'psutil==5.9.0']

if sys.platform == "darwin":
    requirements += ["pyobjc-framework-Quartz==8.5"]

setup(
    name='PyGetWindow',
    version=version,
    url='https://github.com/asweigart/pygetwindow',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('A simple, cross-platform module for obtaining GUI information on application\'s windows.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    test_suite='tests',
    install_requires=requirements,
    keywords="gui window geometry resize minimize maximize close title",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
