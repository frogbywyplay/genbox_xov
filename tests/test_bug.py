#!/usr/bin/env python
#
# Copyright (C) 2006-2013 Wyplay, All Rights Reserved.
#
import sys
import os
import shutil
import unittest
from os.path import realpath, dirname
from subprocess import Popen, PIPE

curr_path = realpath(dirname(sys.modules[__name__].__file__))

class xovScriptTester(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        self.tgt_dir = curr_path + '/targets'
        self.fake_tgt = "%s/fake" % self.tgt_dir
        self.xov = '%s/scripts/xov' % (curr_path + '/..')

    def _set_add_args(self):
        xov_args = "%s --add foo --cfg-dir %s/etc --ov-dir %s/portage --uri dummy --proto mercurial --branch default" % (self.xov, self.fake_tgt, self.fake_tgt)
        self.xov_args = xov_args.split(' ')
        
    def setUp(self):
        self.env = {}
        os.mkdir(self.tgt_dir)
        os.mkdir(self.fake_tgt)
        os.mkdir(self.fake_tgt + '/etc')
        foo = open(self.fake_tgt + '/etc/make.conf', 'a')
        foo.close()

    def tearDown(self):
        shutil.rmtree(self.tgt_dir)
    
    def test_bug5277(self):
        """#5277: xov fails when no current target is set"""
        self.env['TARGETS_DIR'] = self.tgt_dir
        self._set_add_args()
        ret = Popen(self.xov_args, stdout=None, stderr=None, env=self.env).wait()
        self.failUnlessEqual(ret, 0)

if __name__ == '__main__':
    unittest.main()

