import setuptools
import re


__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    open('bluetooth_speaker_bulb/__init__.py').read()
).group(1)

setuptools.setup(
    name='bluetooth_speaker_bulb',
    version=__version__,
    description='Unofficial Python API to control '
                'bluetooth speaker bulb',
    long_description='See https://github.com/orrpan/bluetooth_speaker_bulb for more info,\
         based on Betrees https://github.com/Betree/magicblue',
    url='https://github.com/orrpan/bluetooth_speaker_bulb',
    author='Oskar Joelsson',
    author_email='',
    license='MIT',
    packages=['bluetooth_speaker_bulb'],
    install_requires=[
        'bleak>=0.15.0',
        'webcolors'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bluetooth_speaker_bulb = bluetooth_speaker_bulb.magicblueshell:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
    ],
    keywords=['bluetooth', 'bulb', 'my', 'bluetooth_speaker_bulb', 'blue', 'ble', 'iot']
)
