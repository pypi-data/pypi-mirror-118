from setuptools import setup
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Unix',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='divbasiccalculator',
  version='0.0.2',
  description='A very basic calculator',
  long_description=open('readme.txt').read() + '\n\n' + open('changelog.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Divit Kanath',
  author_email='divitkanath@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=['divcalc'],
  include_package_data=True,
  install_requires=[''] 
)