#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides kalasiris *_k functions*.

   The kalasiris *_k functions* provide some syntactic sugar to make
   calling the ISIS programs just that much easier.  For example here
   are two ways to do the same thing::

        import kalasiris as isis

        cube_file = 'some.cub'

        keyval = isis.getkey(cube_file, grpname='Instrument',
                         keyword='InstrumentId').stdout.strip()

        k_keyval = isis.getkey_k(cube_file, 'Instrument', 'InstrumentId')

   And the values of ``keyval`` and ``k_keyval`` are identical, its
   just that the *_k function* version is a little more compact.
   Each of the *_k functions* implements their modifications a
   little differently, so make sure to read their documentation.
"""

# Copyright 2019, Ross A. Beyer (rbeyer@seti.org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tempfile
import os
from pathlib import Path

import kalasiris as isis


def getkey_k(cube: os.PathLike, group: str, key: str) -> str:
    '''Simplified calling for getkey.

    No default parameters are needed, and it directly returns a string.
    '''
    return(isis.getkey(cube, grpname=group, keyword=key).stdout.strip())


def hi2isis_k(*args, **kwargs):
    '''Creates a default name for the to= cube.

    If the FROM file has the name ``foo.img``, then the output will be ``foo.cub``.'''
    from_path = Path()
    if len(args) > 0 and not str(args[0]).endswith('__'):
        from_path = Path(args[0])
    else:
        for(k, v) in kwargs.items():
            if 'from_' == k:
                from_path = Path(v)
    if 'to_' not in kwargs:
        kwargs.setdefault('to', from_path.with_suffix('.cub'))
    return(isis.hi2isis(*args, **kwargs))


def hist_k(*args, **kwargs) -> str:
    '''Returns the contents of the file created by ISIS hist as a string.

       If there is a TO= parameter in the arguments, ``hist_k()`` will
       create the file, and return its contents as a string
    '''
    to_pathlike = None
    for (k, v) in kwargs.items():
        if 'to' == k or 'to_' == k:
            to_pathlike = v

    f = None
    if not to_pathlike:
        f = tempfile.NamedTemporaryFile(mode='w+')
        kwargs['to'] = f.name

    isis.hist(*args, **kwargs)

    if not f:
        f = open(to_pathlike, 'r')
    contents = f.read()
    f.close()

    return contents
