from setuptools import setup
with open("README.MD", "r") as f:
    long_description= f.read()
setup(name='Brainshop',
version='0.0.4',
description='An easy to use API wrapper for Brainshop.ai',
long_description=long_description,
long_description_content_type = "text/markdown",
author='Rishikesh',
packages=['Brainshop'],
install_requires=['requests'])
