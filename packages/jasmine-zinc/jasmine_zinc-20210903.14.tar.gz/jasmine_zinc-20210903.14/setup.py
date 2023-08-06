from setuptools import setup, find_packages
import sys
from typing import (
    List,
)

from jasmine_zinc import __VERSION__ as VERSION

install_requires: List[str] = [
    # dependencies like requirements.txt
    'requests', # https://pypi.org/project/requests
    'playsound', # https://pypi.org/project/playsound
]

python_version = sys.version_info
if python_version < (3, 7):
    # backport for dataclasses, https://pypi.org/project/dataclasses/
    install_requires += [ 'dataclasses>=0.8' ]

setup(
    name='jasmine_zinc',
    version=VERSION,
    license='MIT',

    packages=find_packages(),
    include_package_data=True,

    entry_points = {
        'console_scripts': [
            'jaz_get_avatars = jasmine_zinc.scripts.get_avatars:main',
            'jaz_talk_on_server = jasmine_zinc.scripts.talk_on_server:main',
            'jaz_record_talk = jasmine_zinc.scripts.record_talk:main',
        ],
    },

    install_requires=install_requires,

    author='aoirint',
    author_email='aoirint@gmail.com',

    url='https://github.com/aoirint/jasmine_zinc',
    description='',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
