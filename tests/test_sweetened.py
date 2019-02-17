#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sweetened` module."""

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

import os
import unittest
import kalasiris.sweetened as isis


# Hardcoding this, but I sure would like a better solution.
img = os.path.join('test-resources', 'HiRISE_test.img')


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        self.assertTrue(os.path.isfile(img))


class Test_hi2isis(unittest.TestCase):

    def setUp(self):
        self.img = img

    def tearDown(self):
        os.remove('print.prt')

    def test_hi2isis_with_to(self):
        tocube = 'test_hi2isis.cub'
        isis.hi2isis(self.img, to=tocube)
        self.assertTrue(os.path.isfile(tocube))
        os.remove(tocube)

    def test_hi2isis_without_to(self):
        tocube = os.path.splitext(self.img)[0] + '.cub'
        isis.hi2isis(self.img)
        self.assertTrue(os.path.isfile(tocube))
        os.remove(tocube)


class Test_getkey(unittest.TestCase):

    def setUp(self):
        self.cub = 'test_getkey_k.cub'
        isis.hi2isis(img, to=self.cub)

    def tearDown(self):
        os.remove(self.cub)
        os.remove('print.prt')

    def test_getkey_k(self):
        truth = 'HIRISE'
        key = isis.getkey(self.cub, 'Instrument', 'InstrumentId')
        self.assertEqual(truth, key)
