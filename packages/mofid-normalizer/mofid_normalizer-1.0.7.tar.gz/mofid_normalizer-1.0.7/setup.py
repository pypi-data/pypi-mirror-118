from setuptools import find_packages, setup
# read the contents of your README file
from os import path
from mofid_normalizer.version import __version__
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

exec(open('mofid_normalizer/version.py').read())
setup(
    name='mofid_normalizer',
    packages=find_packages(include=['mofid_normalizer']),
    version= __version__,
    install_requires=["nltk", "num2fawords", "spacy", "googledrivedownloader"],
    description='first version of Mofid Normalizer',
    author='ali96ebrahimi@gmail.com',
    license='MIT',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
