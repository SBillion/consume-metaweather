from setuptools import setup, find_packages

setup(
    name='weather',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'inquirer',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        weather=weather:main
    ''',
)