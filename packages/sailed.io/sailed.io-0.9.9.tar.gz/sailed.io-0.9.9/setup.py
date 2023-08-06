from setuptools import setup
from setuptools import find_packages
import os, pathlib

from sail import config

p = pathlib.Path(__file__)
p = p.parent.resolve()
requirements = str(p) + '/requirements.txt'

with open(requirements) as f:
	install_reqs = f.read().splitlines()

setup(
	name='sailed.io',
	version=config.VERSION,
	description='A CLI service and toolkit to deploy WordPress to DigitalOcean',
	author='Konstantin Kovshenin',
	author_email='kovshenin@gmail.com',
	install_requires=install_reqs,
	packages=find_packages(),
	entry_points={
		'console_scripts': ['sail=sail.cli:cli']
	},
)
