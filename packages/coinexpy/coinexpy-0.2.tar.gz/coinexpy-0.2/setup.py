# from distutils.core import setup
from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='coinexpy',
    packages=['coinexpy'],
    version='0.2',
    license='MIT',
    description='Python wrapper for Coinex APIs',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Iman Mousaei',
    author_email='imanmousaei1379@gmail.com',
    url='https://github.com/imanmousaei/coinexpy',
    download_url='https://github.com/imanmousaei/coinexpy/archive/refs/tags/v0.2-alpha.tar.gz',
    keywords=['coinex', 'api', 'wrapper', 'trade', 'crypto', 'bitcoin'],
    install_requires=[
        'hashlib',
        'json',
        'urllib3'
    ],
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
