from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sales_billing/__init__.py
from sales_billing import __version__ as version

setup(
	name="sales_billing",
	version=version,
	description="Summary of sales invoices to send to customer in batch",
	author="FLO",
	author_email="kittiu@ecosoft.co.th",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
