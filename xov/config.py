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
import exceptions
import os
import re
import overlay
import xtarget

class XovConfigError(exceptions.Exception):
	"""Error class to Xov."""
	def __init__(self, error=None):
		self.error = error
	def __str__(self):
		if self.error:
			return self.error
		else:
			return ""

class XovConfig(object):
	def __init__(self, cfg_dir, ov_dir, is_targets=False):
		self.cfg_dir = cfg_dir
		self.cfg_file = self.cfg_dir + (xtarget.consts.XTARGET_SYS_OV_CFG[4:] if is_targets else '/xov.conf')
		self.ov_dir = ov_dir
		self.ov_re = re.compile('^PORTAGE_(.*)_(.*)="(.*)"$')
		self.portdir_re = re.compile(r'^\s*PORTDIR\s*=\s*(?P<dbl>\")(?P<value>(?:[^\\"]|\\.)*)(?(dbl)\")')
		self.portdir_ov_re = re.compile('PORTDIR_OVERLAY\s*=\s*"([^"]*)"')
		pass

	def __ov_config(self, line, ovs):
		elems = self.ov_re.split(line)
		name = elems[1].lower()
		if not ovs.has_key(name):
			ovs[name] = overlay.Overlay()
		ovs[name].name = name
		if elems[2] == "PROTO":
			ovs[name].protocol = elems[3]
		elif elems[2] == "URI":
			ovs[name].uri = elems[3]
		elif elems[2] == "REVISION":
			ovs[name].revision = elems[3]
		elif elems[2] == "BRANCH":
			ovs[name].branch = elems[3]
		else:
			return 1
		return 0

	def __ov_portdir(self, line, ovs):
		portdir = self.portdir_re.match(line).group('value')
		name = os.path.basename(portdir)
		if not ovs.has_key(name):
			ovs[name] = overlay.Overlay()
		ovs[name].set_portdir()

	def read(self):
		ovs = {}
		# debug
		if os.path.isfile(self.cfg_file): 
			fd = open(self.cfg_file, 'r')
			for ii in fd.readlines():
				if self.ov_re.match(ii):
					self.__ov_config(ii, ovs)
				elif self.portdir_re.match(ii):
					self.__ov_portdir(ii, ovs)
			fd.close()
		return ovs
	
	def write(self, ovs):
		fd = open(self.cfg_file, 'w')
		paths = []
		portdir = None
		for ii in ovs.values():
			ii.write(fd)
			if (ii.is_portdir() and not portdir):
				portdir = 'PORTDIR="%s/%s"\n' % (self.ov_dir, ii.name)
			else:
				paths.append(self.ov_dir + '/' + ii.name)
		# set PORTDIR_OVERLAY variable
		overlays = 'PORTDIR_OVERLAY="\n'
		overlays += '$PORTDIR_OVERLAY\n'
		overlays += '\n'.join(paths) + '\n'
		overlays += '"'
		print >> fd, "# portage configuration"
		if portdir:
			print >> fd, portdir
		print >> fd, overlays
		fd.close()

