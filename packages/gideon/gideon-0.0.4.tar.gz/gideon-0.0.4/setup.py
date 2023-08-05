from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='gideon',
  version='0.0.4',
  description='simple gideon library for python3 and python2',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Overnice.exe',
  author_email='silkepilon2009@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  packages=find_packages(),
  install_requires=['requests', 'colorama', 'pyttsx3', 'SpeechRecognition', 'neuralintents', 'typing'] 
)
