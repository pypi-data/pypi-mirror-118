import codecs
import os.path
import re

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as f:
        content = f.read()
    return content


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(
    name='takenoko',
    version=find_version('takenoko', '__init__.py'),
    description='takenoko',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='arukisumaho',
    url='https://github.com/fuku2014/takenoko',
    packages=find_packages(),
    package_data={'takenoko': ['data/*.json']},
    include_package_data=True,
    install_requires=[],
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ),
)
