import os
import setuptools
requiredPackages = [
    'requests'
]

for p in requiredPackages:
    os.system('pip3 install {} -q'.format(p))


import utils
setuptools.setup(
    name='utils-S',
    version=utils.version,
    author="Sal Faris",
    description="Utility functions",
    packages=setuptools.find_packages(),
    license='MIT',
    author_email='salmanfaris2005@hotmail.com',
    url='https://github.com/The-Sal/utils/',
    download_url='https://github.com/The-Sal/utils/archive/refs/tags/v1.6.4.tar.gz'
)
