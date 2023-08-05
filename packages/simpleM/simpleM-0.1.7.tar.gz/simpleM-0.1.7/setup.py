from setuptools import setup, find_packages
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

VERSION = '0.1.7' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        print('hello,world, post')
        install.run(self)
    
# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="simpleM", 
        version=VERSION,
        author="qiujingyu",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        data_files=[('.simpleM', ['doc/a/b.txt'])],
        package_data={'simpleM': ['1234.txt','data/*']},

        entry_points = {
            'console_scripts': ['simpleM=simpleM.display:f'],
        },

        cmdclass={
            'install': PostInstallCommand,
        },

)