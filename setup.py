import os
from setuptools import setup

setup(
    name='commandment',
    packages=['commandment'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    package_data={'config': ['config/config.json']}
)
