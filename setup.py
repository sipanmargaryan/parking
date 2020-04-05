from setuptools import setup, find_packages
setup(
    name='parking',
    version='0.1',
    package_dir={'': 'apps', 'project': './project', 'core': './apps/core'},
    packages=find_packages('apps') + ['project', 'core'],
)
