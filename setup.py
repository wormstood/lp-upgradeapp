"""
Setup script for UpgradeApp.
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='upgradeapp',
    version='0.1.0',
    author='wormstood',
    description='A tool for upgrading applications, Docker, and Podman containers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wormstood/lp-upgradeapp',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    install_requires=[
        # No external dependencies for basic template
    ],
    entry_points={
        'console_scripts': [
            'upgradeapp=main:main',
        ],
    },
)
