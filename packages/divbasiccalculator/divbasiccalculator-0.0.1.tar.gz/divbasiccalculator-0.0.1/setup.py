from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Unix',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='divbasiccalculator',
  version='0.0.1',
  description='A very basic calculator',
  long_description=open('readme.txt').read() + '\n\n' + open('changelog.txt').read(),
  url='',  
  author='Divit Kanath',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[''] 
)