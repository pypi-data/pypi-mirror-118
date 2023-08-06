import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myHalo",
    version="1.0.1",
    author="Hongson Tian",
    author_email="hongsontian@zego.im",
    description="print halo",
    long_description=long_description,
    url="https://github.com/hongcheng88/.github.io.git",
    packages=['printHalo'],
    install_requires=['requests', 'pyaml'],
    entry_points={
        'console_scripts': [
            'douyin_image=douyin_image:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)