import setuptools
import sys

if '--release' in sys.argv:
    zipsafe = True
else:
    zipsafe = False

setuptools.setup(
    name='pyths',
    version='0.0.0',
    description='2H Suspense Drama',
    packages=setuptools.find_packages(),
    zip_safe=zipsafe
)
