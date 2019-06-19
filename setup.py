from setuptools import find_packages, setup

with open("README.md", "r") as f:
	long_description = f.read()





setup(
	name="sneaky_snek",
	version="0.1.2",
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	py_modules=["watchFolders"],
	#package_dir={'': 'watchFolders'},
	install_requires=[
		'watchdog'
	],
	package_data={
		'': ['sneaky_snek/injectors', '../LICENSE']
	},
  	long_description=long_description,
	long_description_content_type="text/markdown",
	description="Watches Python projects and refreshes pages in a browser.",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GPL-3.0",
		"Operating System :: OS Independent",
	],
)