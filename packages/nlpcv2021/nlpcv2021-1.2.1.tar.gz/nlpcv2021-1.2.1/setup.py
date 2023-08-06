from distutils.core import  setup
import setuptools
packages = ['nlpcv2021']# 唯一的包名，自己取名
setup(name='nlpcv2021',
	version='1.2.1',
	author='yy',
    packages=packages, 
    package_dir={'requests': 'requests'},)
