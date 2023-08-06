from setuptools import setup
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Unix',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  'Programming Language :: Python :: 3.9'
]
 
setup(
  name='enpy',
  version='1.0.0',
  description='An encryption/decryption program that incorporates OTP',
  long_description=open('readme.md').read() + '\n\n' + open('changelog.md').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Divit Kanath',
  author_email='divitkanath@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['encryption', 'decryption'], 
  packages=['enpy'],
  include_package_data=True,
  install_requires=[''] 
)