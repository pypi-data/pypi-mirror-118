from setuptools import setup, find_packages

setup(
    name='as_project',
    version='0.1.3',    
    description='Enlighten coding project--alphabet soup',
    author='Charlene DiMiceli',
    author_email='cdimicel@umd.edu',
    packages=['as_project', 'as_project.test'],
    scripts=['./bin/given.py'],
    package_data={'': ['*.txt', '*.out']},
    install_requires=[
                      'numpy',
                      ],

)
