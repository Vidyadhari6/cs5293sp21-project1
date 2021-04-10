from setuptools import setup, find_packages

setup(
	name='project1',
	version='1.0',
	author='Vidyadhari',
	author_email='vidyadhari.maddukuri@ou.edu',
	packages=find_packages(exclude=('tests')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']
)