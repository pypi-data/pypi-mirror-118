from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='superglobals',
    version='0.0.2',
    packages=['superglobals'],
    url='https://github.com/sfinktah/superglobals',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Christopher Anderson',
    author_email='sfinktah@github.spamtrak.org',
    description='globals() access anywhere',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
)
