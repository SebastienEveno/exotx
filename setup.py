from setuptools import setup, find_packages

with open('README.md', 'r', encoding="utf-8", errors='ignore') as fh:
    long_description = fh.read()

version = {}
with open("exotx/_version.py", encoding="utf-8") as fp:
    exec(fp.read(), version)

setup(name='exotx',
      version=version['__version__'],
      description='Python library for pricing autocallables',
      author='Sebastien Eveno',
      author_email='sebastien.louis.eveno@gmail.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/SebastienEveno/exotx',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy>=1.16.5',
          'pandas',
          'scipy',
          'matplotlib',
          'plotly>=4.12.0',
          'quantlib>=1.26'
      ],
      python_requires='>=3.6, <4',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis'
        ]
      )