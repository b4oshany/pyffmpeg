import os

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
import subprocess

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.md')).read()
except IOError:
    CHANGES = ''

version = '0.7.0dev'

install_requires = []

class CustomInstallCommand(install):
    """Custom install setup to help run shell commands (outside shell) before installation"""
    def run(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        output = subprocess.Popen("%s/install.sh" % dir_path,
                                  shell = True, stdout =
                                  subprocess.PIPE).stdout.read()
        install.run(self)


setup(
    name='pyffmpeg',
    version=version,
    description="FFMPEG Support for python",
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Sign Lanuage :: Videos",
        "License :: Repoze Public License",
    ],
    author='Oshane Bailey',
    author_email='b4.oshany@gmail.com',
    url='https://github.com/b4oshany/voscrape',
    keywords='splitter videos ffmpeg',
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=["pyffmpeg"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[],
    dependency_links=[],
    entry_points={},
    extras_require={},
)
