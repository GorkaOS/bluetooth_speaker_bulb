import setuptools
import re


__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    open('mylight/__init__.py').read()
).group(1)

setuptools.setup(
    name='mylight',
    version=__version__,
    description='Unofficial Python API to control '
                'MyLight bulbs over Bluetooth',
    long_description='See https://github.com/orrpan/mylight for more info,\
         based on Betrees https://github.com/Betree/magicblue',
    url='https://github.com/orrpan/mylight',
    author='Oskar Joelsson',
    author_email='',
    license='MIT',
    packages=['mylight'],
    install_requires=[
        'bluepy==1.1.4',
        'webcolors'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mylight = mylight.magicblueshell:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
    ],
    keywords=['bluetooth', 'bulb', 'my', 'mylight', 'blue', 'ble', 'iot']
)
