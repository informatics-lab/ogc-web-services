#!/usr/bin/env python

from setuptools import setup

setup(name='webcoverageservice',
      version='0.1.0',
      install_requires=["requests >= 2.3.0",
                        "python-dateutil"],
      description='Python interface to web coverage services',
      author='Met Office Informatics Lab',
      maintainer='Met Office Informatics Lab',
      url='https://github.com/met-office-lab/ogc-web-services',
      license='TBC',
      packages=['webcoverageservice',
                'webcoverageservice/builders',
                'webcoverageservice/readers',
                'webcoverageservice/senders'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ]
     )
