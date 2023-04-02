from setuptools import setup

with open("README.md", 'r') as f:
   long_description = f.read()

setup(
   name='Password Manager',
   version='1.0',
   description='A local password manager.',
   license='MIT',
   long_description=long_description,
   author='Alessandro Ravizzotti',
   author_email='alessandro@ravizzotti.dev',
   url='https://github.com/itsraval/passwordManagerSB/',
   install_requires=['Pillow', 'pyperclip', 'passlib', 'pycryptodome'],
   python_requires=">=3.8",
)