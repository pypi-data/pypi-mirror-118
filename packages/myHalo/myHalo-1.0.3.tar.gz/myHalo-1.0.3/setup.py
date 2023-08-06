import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myHalo",
    version="1.0.3",
    author="Hongson Tian",
    author_email="hongsontian@zego.im",
    description="print halo",
    long_description=long_description,
    url="https://pypi.org/project/myHalo/",
    packages=['printHalo'],
    install_requires=['requests', 'pyaml'],
    entry_points={
        'console_scripts': [
            'print_halo=printHallo:main'
        ],
    },
    classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
