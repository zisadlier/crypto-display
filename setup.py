from setuptools import setup

setup(
    name='cryptodisplay',
    version='0.1.0',
    packages=['cryptodisplay'],
    include_package_data=True,
    install_requires=[
        "coinmarketcap==4.1.2",     
    ],
    entry_points={
        'console_scripts': [
            'cryptodisplay = cryptodisplay.__main__:main'
        ]
    },
)