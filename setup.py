from setuptools import setup
import sys

if ( sys.version_info[0] == 2 ):
    tkinterPackage = "Tkinter"
else:
    tkinterPackage = "tkinter"

setup(
    name='PLOD',
    version='1.0',
    description='Matplotlib plot designer',
    author='David Kleiven',
    licence='MIT',
    author_email='davidkleiven446@gmail.com',
    install_requires=['numpy', 'matplotlib','subprocess'], # Requires also Tkinter (or tkinter), but is part of the standard library
    url='https://github.com/davidkleiven/PLOD',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    #py_modules=['plotHandler', 'controlGUI'],
    packages=['PLOD']
)
