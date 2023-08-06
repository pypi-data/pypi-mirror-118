from setuptools import setup
# from unitgrade import version
# version = "0.0.1"
from unitgrade import __version__ as version
setup(
    name='unitgrade',
    version=version,
    packages=['unitgrade', 'cs101courseware_example'],
    url='https://lab.compute.dtu.dk/tuhe/unitgrade',
    license='Apache', 
    author='Tue Herlau',
    author_email='tuhe@dtu.dk',
    description='A lightweight student evaluation framework build on unittest',
    install_requires=['jinja2', 'tabulate', 'sklearn', 'compress_pickle', ],
    # include_package_data=False,
    # package_data={'', ['*.dat']},#'cs101courseware_example/Report1_resources_do_not_hand_in.dat', 'cs101courseware_example/Report2_resources_do_not_hand_in.dat')},
)
