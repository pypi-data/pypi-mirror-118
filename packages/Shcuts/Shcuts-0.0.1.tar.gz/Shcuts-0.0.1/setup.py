from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Shcuts',
  version='0.0.1',
  description='Some fun and helpful shortcuts',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Daniel Hambach',
  author_email='daniel@hambach.org',
  license='MIT', 
  classifiers=classifiers,
  keywords='shortcuts', 
  packages=find_packages(),
  install_requires=[''] 
)