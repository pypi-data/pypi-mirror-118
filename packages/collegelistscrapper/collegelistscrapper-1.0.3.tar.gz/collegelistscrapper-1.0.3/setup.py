from setuptools import setup, find_packages

VERSION = '1.0.3' 
DESCRIPTION = 'Turns college Search results into excel file.'
LONG_DESCRIPTION = 'It turns niche college search into excel or csv'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="collegelistscrapper", 
        version=VERSION,
        author="Apocryphal",
        author_email="apocryphal.work.923@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas', 'requests', 'bs4', 'html5lib', 'xlsxwriter'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['scrapper', 'colleges', 'collegelistsscrapper', 'niche'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)