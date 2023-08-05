from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.1',
  'Programming Language :: Python :: 3.2',
  'Programming Language :: Python :: 3.3',
  'Programming Language :: Python :: 3.4',
  'Programming Language :: Python :: 3.5',
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8'
]
 
setup(
  name='kisaan',
  version='0.2.1',
  description='A very basic discription',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Joshua Lowe',
  author_email='josh@edublocks.org',
  license='MIT', 
  classifiers=classifiers,
  keywords="kisaan",
  packages=find_packages(),
  install_requires=["pymongo[srv]==3.11.4","asyncio==3.4.3"]
)
