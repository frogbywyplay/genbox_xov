#!/usr/bin/python
#
# Copyright (C) 2006-2014 Wyplay, All Rights Reserved.
# This file is part of xov.
# 
# xov is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# xov is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see file COPYING.
# If not, see <http://www.gnu.org/licenses/>.
#
#

import unittest
import sys, os

curr_path = os.path.realpath(os.path.dirname(sys.modules[__name__].__file__))

sys.path.insert(0, curr_path + '/..')
import xov.xov as x

TMPDIR = curr_path + '/tmp_dir'
OV_URI = 'ssh://hg@sources/genbox/overlays/ov-dev-tools'
OV_PROTO = 'mercurial'
OV_BRANCH = 'default'

class xovAddTester(unittest.TestCase):
        def __init__(self, methodName='runTest'):
                unittest.TestCase.__init__(self, methodName)
                self.path = os.path.realpath(os.path.dirname(sys.modules[__name__].__file__))

        def setUp(self):
                os.system('rm -rf %s' % TMPDIR)
                os.mkdir(TMPDIR)
                f = open(TMPDIR + '/make.conf', 'w')
                f.close()

        def tearDown(self):
                os.system('rm -rf %s' % TMPDIR)

        def testAddForce(self):
                xov = x.Xov(TMPDIR, TMPDIR, sys.stdout, sys.stderr)
                xov.add('test', OV_URI, OV_PROTO, branch=OV_BRANCH, force=False)

                try:
                        xov.add('test', OV_URI, OV_PROTO, branch=OV_BRANCH, force=False)
                        self.fail('An error should have been raised')
                except x.XovError:
                        pass
                xov.add('test', OV_URI, OV_PROTO, branch=OV_BRANCH, force=True)


if __name__ == "__main__":
        unittest.main()

