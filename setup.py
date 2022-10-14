import setuptools
import re


__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    open('alloyseed/__init__.py').read()
).group(1)

setuptools.setup(
    name='alloyseed',
    version=__version__,
    description='Unofficial Python API to control '
                'Alloyseed bulbs over Bluetooth',
    long_description='See https://github.com/orrpan/alloyseed for more info,\
         based on Betrees https://github.com/Betree/magicblue',
    url='https://github.com/orrpan/alloyseed',
    author='Oskar Joelsson',
    author_email='',
    license='MIT',
    packages=['alloyseed'],
    install_requires=[
        'bleak>=0.15.0',
        'webcolors'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'alloyseed = alloyseed.magicblueshell:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
    ],
    keywords=['bluetooth', 'bulb', 'my', 'alloyseed', 'blue', 'ble', 'iot']
)
