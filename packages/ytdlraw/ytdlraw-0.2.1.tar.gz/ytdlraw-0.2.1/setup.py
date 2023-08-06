from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10 ',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ytdlraw',
  version='0.2.1',
  description='A barebones YouTube Downloader',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
  url='',  
  author='DS_Stift007',
  author_email='dsstif@icloud.org',
  license='MIT', 
  classifiers=classifiers,
  keywords=['youtube','download','ytdl'], 
  packages=find_packages(),
  install_requires=['pytube'] 
)