from setuptools import setup

setup(
   name='hpc4ag',
   version='1.0',
   description='Functions used in the hpc4ag class',
   author='Olena Boiko',
   author_email='oboiko@umn.edu',
   packages=['hpc4ag'],
   install_requires=['matplotlib', 'numpy', 'seaborn', 'scikit-learn', 'tensorflow'],
)