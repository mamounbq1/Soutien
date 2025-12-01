"""
Script d'installation pour le Système de Gestion - Centre de Soutien Scolaire
"""

from setuptools import setup, find_packages
import os

# Lire le README
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# Lire les requirements
def read_requirements():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='soutien-scolaire-manager',
    version='2.0.0',
    author='Mamoun BQ',
    author_email='contact@example.com',
    description='Système de gestion complet pour centre de soutien scolaire',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/mamounbq1/Soutien',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'soutien-manager=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt', '*.json'],
    },
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
)
