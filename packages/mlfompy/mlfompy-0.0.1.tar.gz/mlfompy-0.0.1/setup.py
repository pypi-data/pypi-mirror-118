import setuptools
from distutils.command.install_data import install_data
import os, re


#####VERSION CONTROL#####

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

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


setuptools.setup(
    name='mlfompy',
    #cmdclass={'install_data': custom_install},
    version=find_version("src", "mlfompy", "__init__.py"),
    description='MLFoMPy is an effective tool that extracts the main figures of merit (FoM) of a semiconductors IV curve',
    author='',
    author_email='',
    url='https://gitlab.citius.usc.es/modev/mlfompy',
    setup_requires=['setuptools','numpy'],
    install_requires=['scipy','pytest','probscale', 'matplotlib'],
    package_dir={"": "src"},
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


