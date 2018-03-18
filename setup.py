#! /usr/bin/env python3

####################################################################################################
#
# Climbing Asso Portal - A Portal for Climbing Club (Association)
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import glob
import sys

from setuptools import setup, find_packages
setuptools_available = True

####################################################################################################

if sys.version_info < (3,):
    print('ClimbingAssoPortal requires Python 3', file=sys.stderr)
    sys.exit(1)
if sys.version_info < (3,5):
    print('WARNING: ClimbingAssoPortal could require Python 3.5 ...', file=sys.stderr)

####################################################################################################

exec(compile(open('setup_data.py').read(), 'setup_data.py', 'exec'))

####################################################################################################

setup_dict.update(dict(
    # include_package_data=True, # Look in MANIFEST.in
    packages=find_packages(exclude=['unit-test']),
    scripts=glob.glob('bin/*'),
    # [
    #     'bin/...',
    # ],
    package_data={
        'ClimbingAssoPortal.Config': ['logging.yml'],
        'ClimbingAssoPortal.Spice.NgSpice': ['api.h'],
    },

    platforms='any',
    zip_safe=False, # due to data files

    classifiers=[
        "Topic :: Other/Nonlisted Topic",
        "Intended Audience :: Other Audience",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.5',
        ],

    install_requires=[
        # 'Django',
    ],
))

####################################################################################################

setup(**setup_dict)
