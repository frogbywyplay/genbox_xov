#!/usr/bin/env python 
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
import sys
import os
import shutil
import unittest

curr_path = os.path.realpath(os.path.dirname(sys.modules[__name__].__file__))

sys.path.insert(0, curr_path + '/..')

from xov.xov import Xov, XovError
from xov.config import XovConfig
from xov.overlay import OverlayError

class xovTester(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
	self.cfg_write_dir = curr_path + '/cfg_write'
	self.ov_dir = curr_path + '/overlays'
	self.make_conf = self.cfg_write_dir + '/make.conf'

    def _create_portage_config(self):
	if not os.path.isfile(self.make_conf):
		foo = open(self.make_conf, 'a')
		foo.close()
	
    def _delete_portage_config(self):
	if os.path.isfile(self.make_conf):
		os.unlink(self.make_conf)

    def setUp(self):
    	os.mkdir(self.cfg_write_dir)
	os.mkdir(self.ov_dir)
	self._create_portage_config()

    def tearDown(self):
    	shutil.rmtree(self.ov_dir)
	shutil.rmtree(self.cfg_write_dir)

    def testRead(self):
	"""Check config file reading"""
	self.xov = Xov(curr_path + '/cfg', curr_path + '/overlays')
	self.failUnless(self.xov.ovs.has_key('wms'))
	self.failUnless(self.xov.ovs.has_key('a1'))
	# check for wms value
	self.failUnlessEqual(self.xov.ovs['wms'].protocol, 'mercurial')
	self.failUnlessEqual(self.xov.ovs['wms'].uri, 'ssh://hg@sources.wyplay.int/genbox/overlays/ov-wms')
	self.failUnlessEqual(self.xov.ovs['wms'].branch, '1.4.0')
	self.failUnless(self.xov.ovs['wms'].revision is None)
	self.failUnless(self.xov.ovs['wms'].is_portdir())
	# check for a1 value
	self.failUnlessEqual(self.xov.ovs['a1'].protocol, 'mercurial')
	self.failUnlessEqual(self.xov.ovs['a1'].uri, 'ssh://hg@sources.wyplay.int/genbox/overlays/ov-x1')
	self.failUnlessEqual(self.xov.ovs['a1'].branch, '1.4.0')
	self.failUnless(self.xov.ovs['a1'].revision is None)
	self.failIf(self.xov.ovs['a1'].is_portdir())
    
    def testWrite(self):
	"""Check config file writing"""
	self.fail("Test not implemented")

    def testList(self):
        """Check xov list behaviour"""
	self.xov = Xov(curr_path + '/cfg', curr_path + '/overlays')
	ovs = self.xov.list()
        self.failUnless(ovs.has_key('wms'))
	self.failUnless(ovs.has_key('a1'))
        
    def testAdd_Missing_make_conf(self):
    	"""Check behaviour when make.conf is missing"""
	self._delete_portage_config()
	self.xov = Xov(curr_path + '/cfg_write', curr_path + '/overlays')
	self.failUnlessRaises(XovError, self.xov.add, 'abc', 'foo', 'mercurial', 'default')

    def testAdd(self):
        """Check xov add behaviour"""
	self.xov = Xov(curr_path + '/cfg_write', curr_path + '/overlays')
	self.xov.add('abc', 'foo', 'mercurial', 'default')
	self.failUnlessRaises(XovError, self.xov.add, 'abc', 'foo', 'mercurial', 'default')
    	self.failUnlessRaises(OverlayError, self.xov.add, 'a1', 'foo', 'boom', 'default')
        
    def testRm(self):
        """Check xov rm behaviour"""
        self.fail("Test not implemented")
        
    def testSync(self):
        """Check xov sync behaviour"""
        self.fail("Test not implemented")

if __name__ == "__main__":
    unittest.main()

