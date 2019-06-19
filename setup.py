from setuptools import find_packages, setup

with open("README.md", "r") as f:
	long_description = fh.read()

setup(
	name="sneaky-snek",
	version="0.0.1",
	#packages=find_packages(),
	#include_package_data=True,
	#zip_safe=False,
	long_description=long_description,
	long_description_content_type="text/markdown",
	description="Watches Python projects and refreshes pages in a browser.",
	py_modules=['watchFolders'], # modules to be imported
	install_requires=[
		'watchdog'
	],
	package_dir={'':'watcher'} # directory of all the code
)