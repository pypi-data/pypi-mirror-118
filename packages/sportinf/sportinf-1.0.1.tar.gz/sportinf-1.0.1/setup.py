from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sportinf',
    version='1.0.1',
    long_description=long_description,
    packages=['tests', 'sport_info'],
    url='https://github.com/AlexBlackHawk/sportinf',
    license='MIT',
    author='alexm',
    author_email='alex.maudza@gmail.com',
    description='Package to get sport information',
    download_url='https://github.com/AlexBlackHawk/sportinf/archive/refs/tags/1.0.1.tar.gz',
    keywords=['sportinf', 'sport', 'scores', 'statistic'],
    install_requires=['requests'],
    python_requires='>=3'
)
