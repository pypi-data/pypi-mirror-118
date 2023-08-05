from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',  
  'Operating System :: POSIX :: Linux',  
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='klee',
  version='0.0.1',
  description='An an open-source procedural AI and MLOPs library.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='http://klee.ai',  
  author='Nik Bear Brown',
  author_email='nikbearbrown@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='AI,MLOPs', 
  packages=find_packages(),
  install_requires=[''] 
)
