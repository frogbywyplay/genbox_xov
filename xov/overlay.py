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
import exceptions

class OverlayError(exceptions.Exception):
	"""Error class for Overlay"""
	def __init__(self, error=None):
		self.error = error
	def __str__(self):
		if self.error:
			return self.error
		else:
			return ""

class Overlay(object):
        __protocol_set = set(['git', 'mercurial', 'svn'])
        def __init__(self, uri=None, protocol=None, revision=None, branch=None, name=None, is_portdir=False):
                self.uri = uri
                self.revision = revision
		self.branch = branch
                self.name = name
                self._protocol = None
                self.portdir = is_portdir
                # check if protocol is supported
                if protocol:
                    self.protocol = protocol
                
        
        def get_protocol(self):
            return self._protocol
        def set_protocol(self, val):
            if len(Overlay.__protocol_set.intersection(set([val]))) == 0:
                raise OverlayError("Protocol %s is not supported" % val)
            else:
                self._protocol = val

        def set_portdir(self, val=True):
                self.portdir = val

        def is_portdir(self):
                return self.portdir
        
        protocol = property(get_protocol, set_protocol)

        def check_config(self):
            if not self.name:
                raise OverlayError("Name is not set")
            if not self.uri:
                raise OverlayError("Uri is not set")
            if not self.protocol:
                raise OverlayError("Protocol is not set")
            if not (self.revision or self.branch):
                raise OverlayError("Branch or revision must be set")
                return -4
            return 0
	
	def get_env(self):
	    env = {}
	    var_prefix = "PORTAGE_%s" % self.name.upper()
	    env['%s_PROTO' % var_prefix] = "%s" % self.protocol
	    env['%s_URI' % var_prefix] = "%s" % self.uri
	    if self.revision:
	    	env['%s_REVISION' % var_prefix] = "%s" % self.revision
	    if self.branch:
	    	env['%s_BRANCH' % var_prefix] = "%s" % self.branch
	    return env
        def write(self, fd = sys.stdout):
            if self.check_config() < 0:
                return
            var_prefix = "PORTAGE_%s" % self.name.upper()
            print >> fd, "#configuration for overlay %s" % self.name
            print >> fd, '%s_PROTO="%s"' % (var_prefix, self.protocol)
            print >> fd, '%s_URI="%s"' % (var_prefix, self.uri)
	    if self.revision:
            	print >> fd, '%s_REVISION="%s"' % (var_prefix, self.revision)
	    if self.branch:
	    	print >> fd, '%s_BRANCH="%s"' % (var_prefix, self.branch)
            fd.flush()
        
