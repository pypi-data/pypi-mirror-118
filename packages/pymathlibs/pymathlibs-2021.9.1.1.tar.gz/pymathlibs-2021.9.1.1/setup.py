from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pymathlibs',
  version='2021.9.1.1',
  description='PyMathLibs is a free math library in python. This library contains most of the math class libs, and some other features.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='NoobBit',
  author_email='noobbit90@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='math', 
  packages=find_packages(),
  install_requires=[''] 
)