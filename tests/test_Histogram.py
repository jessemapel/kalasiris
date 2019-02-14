#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `Histogram` class."""

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
import kalasiris as isis

# Hardcoding this, but I sure would like a better solution.
# One could download the .img file from the PDS at each setUp,
# but that seems like a lot of network traffic, when you could just
# do it once.
img = 'tests/resources/HiRISE_test.img'


class TestHistogram(unittest.TestCase):

    def setUp(self):
        self.cube = 'test_Histogram.cub'
        self.histfile = 'test_Histogram.hist'
        isis.hi2isis(img, self.cube)
        isis.hist(self.cube, to=self.histfile)

    def tearDown(self):
        os.remove('print.prt')
        os.remove(self.cube)
        os.remove(self.histfile)

    def test_init(self):
        h = isis.Histogram(self.histfile)
        self.assertIsInstance(isis.Histogram, h)

    def test_dictlike(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(self.cube, h['Cube'])

    def test_listlike(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(5, len(h[0]))

    def test_contains(self):
        h = isis.Histogram(self.histfile)
        self.assertTrue('Std Deviation' in h)

    def test_len(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(107, len(h))
