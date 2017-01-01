from setuptools import setup
'''
The packages subprocess and tkinter is also required from the standard library
'''

setup(
    name='PLOD',
    version='1.0',
    description='Matplotlib plot designer',
    author='David Kleiven',
    licence='MIT',
    author_email='davidkleiven446@gmail.com',
    install_requires=['numpy', 'matplotlib'],
    url='https://github.com/davidkleiven/PLOD',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    #py_modules=['plotHandler', 'controlGUI'],
    packages=['PLOD']
)
