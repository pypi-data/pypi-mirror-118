from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='communicationsystemlabtelkom',
  version='0.0.1',
  description='Communication System Lab Telkom University',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Laboratorium Siskom Tel-u',
  author_email='commsylab@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='communication system laboratory', 
  packages=find_packages(),
  install_requires=[''] 
)