"""A setuptools based setup module."""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
        name='matHist',
        version='0.1.1',
        description='A Python script to plot normalized histogram using Python3-Matplotlib',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/sumitavakundu007/matHist',
        author='Sumitava Kundu',
        author_email='kundusumitava@gmail.com',
        classifiers=[
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            ],
        keywords='sample, setuptools, development', 
        packages=['matHist'],
        python_requires='>=3.6',
        install_requires=['numpy', 'matplotlib'],
        
        entry_points={
                'console_scripts': [
                'matHist=matHist.matplotlib_hist:mat_hist_func',
            ],
        },
        
        project_urls={  # Optional
            'Bug Reports': 'https://github.com/sumitavakundu007/matHist/issues',
            'Say Thanks!': 'http://saythanks.io/to/example',
            'Source': 'https://github.com/sumitavakundu007/matHist/',
            },
        )
