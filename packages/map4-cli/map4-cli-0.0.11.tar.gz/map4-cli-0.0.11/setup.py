from setuptools import setup
from glob import glob
from os.path import basename
from os.path import splitext

with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs]

setup(
    name="map4-cli",
    version="0.0.11",
    packages=['src'],
    entry_points={
            "console_scripts": ['map4cli11 = src.root:main']
        },
    install_requires = install_requires,
    description='Map4 CLI Tool',
    long_description=readme,
    url='https://github.com/****',
    author='Rui Hirano',
    author_email='rui.hirano@xxxx.jp',
    license='MIT',
)