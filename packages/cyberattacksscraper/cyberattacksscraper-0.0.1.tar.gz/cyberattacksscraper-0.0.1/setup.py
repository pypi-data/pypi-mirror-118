from setuptools import setup
from setuptools import find_packages

setup(
    name='cyberattacksscraper',
    version='0.0.1', 
    description='Web scraper that scrapes cyber attacks data from the Council on Foreign Relations Cyber Operations Tracker,  .',
    url='https://github.com/anademarr/Software-Engineering-project',
    author='Ana-Maria Dicu',
    license='MIT',
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['selenium', 'pandas', 'sqlalchemy'],
    )


