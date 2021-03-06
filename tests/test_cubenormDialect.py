#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `cubenormDialect` class."""

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

import contextlib
import csv
import unittest
from pathlib import Path

import kalasiris as isis
from .utils import resource_check as rc

# Hardcoding this, but I sure would like a better solution.
img = Path('test-resources') / 'PSP_010502_2090_RED5_0.img'


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        (truth, test) = rc(img)
        self.assertEqual(truth, test)


class TestCubenormDialect(unittest.TestCase):

    def setUp(self):
        self.cube = Path('test_cubenorm.cub')
        self.statsfile = Path('test_cubenorm.stats')
        isis.hi2isis(img, to=self.cube)
        isis.cubenorm(self.cube, stats=self.statsfile)

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()
        self.cube.unlink()
        self.statsfile.unlink()

    def test_cubenorm_reader(self):
        with open(self.statsfile) as csvfile:
            reader = csv.reader(csvfile, dialect=isis.cubenormDialect)
            for row in reader:
                self.assertEqual(8, len(row))
                break
