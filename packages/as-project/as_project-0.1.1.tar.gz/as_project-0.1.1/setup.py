from setuptools import setup, find_packages

setup(
    name='as_project',
    version='0.1.1',    
    description='Enlighten coding project--alphabet soup',
    author='Charlene DiMiceli',
    author_email='cdimicel@umd.edu',
    packages=find_packages(),
    install_requires=[
                      'numpy',
                      ],

    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
