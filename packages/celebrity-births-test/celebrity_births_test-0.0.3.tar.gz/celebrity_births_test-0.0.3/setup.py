from setuptools import setup
from setuptools import find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='celebrity_births_test',
    version='0.0.3',    
    description='Mock package that allows you to find celebrity by date of birth',
    long_description=long_description,
    url='https://github.com/IvanYingX/project_structure_pypi.git',
    author='Ivan Ying',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests', 'beautifulsoup4'],
)