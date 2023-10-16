from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in loan_management/__init__.py
from loan_management import __version__ as version

setup(
	name="loan_management",
	version=version,
	description="loan tracking and managing app",
	author="vignesh",
	author_email="vickystreak@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
