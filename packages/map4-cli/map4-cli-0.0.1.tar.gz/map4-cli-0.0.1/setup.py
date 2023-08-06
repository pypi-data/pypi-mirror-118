from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs]

setup(
    name="map4-cli",
    version="0.0.1",
    packages=['src'],
    entry_points={
            "console_scripts": ['map4cli = src.root:main']
        },
    install_requires = install_requires,
    description='Map4 CLI Tool',
    long_description=readme,
    url='https://github.com/****',
    author='Rui Hirano',
    author_email='rui.hirano@xxxx.jp',
    license='MIT',
)