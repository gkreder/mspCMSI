from setuptools import setup
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()
setup(
   name = 'mspCSMI',
   author = 'gkreder',
   description = 'MSP Parsing',
   version = '0.1.0',
   packages = ['mspCMSI'],
   install_requires = [req for req in requirements if req[:2] != "# "],
   include_package_data=True,
   entry_points = {
      'console_scripts': [
         'mspCSMI = mspCMSI.mspCMSI:main'
      ]
   }
)