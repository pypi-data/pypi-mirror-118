# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 18:44:20 2021

@author: Yongguang Gong
"""

'''
tutorial
0. python setup.py check
1. python setup.py sdist bdist_wheel
2. twine upload dist/*
load: juliangong/gyg3380149
3. https://pypi.org/pypi?%3Aaction=list_classifiers
4. python setup.py develop


'''

import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()
    
setuptools.setup(
    name = "optprc",
    version = "0.2.0",
    author = "Julian Gong",
    author_email = "juliangong@hotmail.com",
    description = "option pricer",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://www.optprc.com",
    # install_requires= ["numpy>=1.22", ],
    
    classifiers = [
            #"Topic::Financial",
            #"Topic::Software Development::Libraries::Python Modules",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
            
    packages = setuptools.find_packages(include = ["optprc","optprc.*"]),
    #install_requires = ["numpy", "scipy", "datetime"],
    include_package_data = True
     
    )

