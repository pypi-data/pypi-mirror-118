from setuptools import setup, find_packages
 
classifiers = [
'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: Open Software License 3.0 (OSL-3.0) ',
  'Programming Language :: Python :: 3',  
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
]
 
setup(
  name='petrabytesunitconverter',
  version='0.0.2',
  description='Can convert scientific units.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read() +'\n\n' + open('Usage.txt').read(),
  url='https://www.petrabytes.com/',  
  author='Lalan Ranjan',
  author_email='lranjan@petrabytes.com',
  license='Petrabytes Corp.', 
  classifiers=classifiers,
  keywords='Unit_Converter', 
  packages=find_packages(),
  install_requires=['pint'] 
)
