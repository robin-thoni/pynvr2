#! /usr/bin/env python3
from os import path
import os

from setuptools import setup, find_packages

install_requires = [
    'argparse',
    'pydantic',
    'pyyaml',
]

here = path.abspath(path.dirname(__file__))


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

setup(
    name='pynvr2',
    version="0.1.0",

    description="Tool to record and rotate video files from various sources",
    long_description="""\
pynvr2-recorder records from any source that is supported by ffmpeg.
pynvr2-janitor rotates video files following user-defined policies.
""",

    url='https://github.com/robin-thoni/pynvr2',
    author="Robin Thoni",
    author_email='robin@rthoni.com',

    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: System Administrators',
        'Topic :: Security',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords="CCTV NVR DVR camera cameras IP",

    packages=find_packages(exclude=['tests*']),
    install_requires=install_requires,

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
    },

    data_files=[
    ],

    entry_points={
        'console_scripts': [
            'pynvr2-recorder=pynvr2.recorder.main:main',
            'pynvr2-janitor=pynvr2.janitor.main:main',
        ],
    },

    cmdclass={
    }
)
