"""
********************************************************************************

Python Script: Blodiator Setup
Writter: Mojtaba Mansour Abadi
Date: 16 July 2019

This Python script is compatible with Python 3.x.
The script is for installing Blodiator.


Histoty:

Ver 0.0.44: 16 July 2019;
             first code

********************************************************************************
"""


# to create the wheel package, run the following in the command line:
# python3 setup.py sdist bdist_wheel


from setuptools import setup, find_packages

setup(name='blodiator',
      version='0.1.00',
      description='block diagram creator',
      long_description='BLOck DIAgram ediTOR (Blodiator) is a package to create block diagrams for free-space optical (FSO) communication system simulator' ,
      classifiers=[
        'Development Status :: 3 - Alpha ',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'TOPIC :: MULTIMEDIA :: GRAPHICS :: EDITORS',
      ],
      keywords='Block diagram editor for graphical UI simulators and processing applications',
      url='https://github.com/MansourM61/Blodiator',
      author='Mojtaba Mansour Abadi',
      author_email='mansourabadi.mojtaba@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      include_package_data=True,
      zip_safe=False)
