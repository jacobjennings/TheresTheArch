"""Setup script for Litematica Python library."""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='litematica-python',
    version='1.0.0',
    author='TheresTheArch',
    description='Python library for reading and writing Litematica schematic files',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/jacob/TheresTheArch',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    install_requires=[
        'NBT>=1.5.0',
    ],
    keywords='minecraft litematica schematic nbt',
    project_urls={
        'Documentation': 'https://github.com/jacob/TheresTheArch/blob/main/litematica-python/README.md',
        'Source': 'https://github.com/jacob/TheresTheArch',
        'Tracker': 'https://github.com/jacob/TheresTheArch/issues',
    },
)

