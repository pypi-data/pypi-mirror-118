from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='moad',
    version='0.2.0',
    packages=['moad'],
    url='https://github.com/claasd/moad',
    license='MIT',
    author='Claas Diederichs',
    author_email='',
    description='Mic open API docs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyYaml"
    ]
)
