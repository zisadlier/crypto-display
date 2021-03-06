"""apt-get install qt5-default pyqt5-dev pyqt5-dev-tools"""

from setuptools import setup

setup(
    name='cryptodisplay',
    version='0.1.0',
    packages=['cryptodisplay'],
    include_package_data=True,
    install_requires=[
        "coinmarketcap==4.1.2",
        "requests==2.18.4",
        "bs4==0.0.1",       
    ],
    entry_points={
        'console_scripts': [
            'cryptodisplay = cryptodisplay.__main__:main'
        ]
    },
)

