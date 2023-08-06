import setuptools
from distutils.command.install_data import install_data
import os, re


#####VERSION CONTROL#####

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version():
    version_str = os.getenv('CI_COMMIT_TAG')
    if version_str:
        version_match = re.search(r"([0-9]+\.[0-9]+\.[0-9]+)",version_str, re.M)
        if version_match:
            return version_match.group(1)
    print("Unable to find version string.")
    return "0.0.0"

#REQUIRES = []
#with open('requirements.txt') as f:
#    for line in f:
#        line, _, _ = line.partition('#')
#        line = line.strip()
#        if ';' in line:
#            requirement, _, specifier = line.partition(';')
#            for_specifier = EXTRAS.setdefault(':{}'.format(specifier), [])
#            for_specifier.append(requirement)
#        else:
#           REQUIRES.append(line)

def get_long_description():
    long_description=''
    with open('README.rst', 'r') as fh:
        long_description=fh.read()
    return long_description

setuptools.setup(
    name='mlfompy',
    version=find_version(),
    description='MLFoMPy is an effective tool that extracts the main figures of merit (FoM) of a semiconductors IV curve',
    long_description=get_long_description(),
    long_description_content_type='text/x-rst',
    author='',
    author_email='',
    url='https://gitlab.citius.usc.es/modev/mlfompy',
    setup_requires=['setuptools','numpy'],
    install_requires=['scipy','pytest','probscale','matplotlib'],
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
    ],
)
# with open('README.rst', 'r') as fh:
#     long_description = fh.read()


# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools


