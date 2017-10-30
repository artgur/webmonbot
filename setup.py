from setuptools import setup

setup(
    name='webmonbot',
    version='0.0.1',
    packages=['webmonbot'],
    package_dir={'webmonbot': 'webmonbot'},
    scripts=[
        'bin/webmonbot'
    ],
    url='',
    license='',
    requires=[
        'requests'
    ],
    tests_require=[
        'pytest',
        'responses'
    ],
    author='artgur',
    author_email='artgur90@gmail.com',
    description=''
)
