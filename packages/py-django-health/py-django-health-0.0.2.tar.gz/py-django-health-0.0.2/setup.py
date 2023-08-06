from distutils.core import setup

setup(
  packages=['health', 'health.checkers'],
  keywords=['health', 'checkers', 'heartbeat', 'microservices'],
  install_requires=[
    'django',
    'pydantic'
  ],
  python_requires=">=3.6",
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ]
)
