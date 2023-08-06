from setuptools import setup, find_packages
 
classifiers = [
'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='com_petrabytes_unit_system',
  version='0.0.2',
  description='Can convert scientific units.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Lalan Ranjan',
  author_email='lranjan@petrabytes.com',
  license='Petrabytes Corp.', 
  classifiers=classifiers,
  keywords='Unit_Converter', 
  packages=find_packages(),
  install_requires=['pint'] 
)
