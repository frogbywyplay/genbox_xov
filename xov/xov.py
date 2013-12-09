#
# Copyright (C) 2006-2013 Wyplay, All Rights Reserved.
#
import exceptions
import os
import re
from subprocess import Popen
import overlay
from config import XovConfig, XovConfigError

class XovError(exceptions.Exception):
	"""Error class to Xov."""
	def __init__(self, error=None):
		self.error = error
	def __str__(self):
		if self.error:
			return self.error
		else:
			return ""

class Xov(object):
	def __init__(self, cfg_dir, ov_dir, stdout=None, stderr=None, root=None):
		self.cfg_dir = cfg_dir
		self.ov_dir = ov_dir
		self.ovs = {}
		self.xov_re = re.compile('^source .*/xov.conf$')
		self.config = XovConfig(cfg_dir, ov_dir)
		if stdout:
			self.stdout = stdout
		else:
			self.stdout = open("/dev/null", "w")
		if stderr:
			self.stderr = stderr
		else:
			self.stderr = open("/dev/null", "w")
                self.root = root
		self._read_config()

	def add(self, name, uri, protocol, revision=None, branch=None, is_portdir=False, force=False):
		if not force and self.ovs.has_key(name):
			raise XovError("Overlay %s already exist" % name)
		self.ovs[name] = overlay.Overlay(uri=uri, protocol=protocol,
						revision=revision, branch=branch,
						name=name, is_portdir=is_portdir)
		# add contains in configuration file
		self._write_config()
		self._update_portage_config()

	def rm(self, name):
		if not self.ovs.has_key(name):
			raise XovError("Overlay %s doesn't exist" % name)
		del self.ovs[name]
		# clean configuration file
		self._write_config()
		self._update_portage_config()
	
	def list(self):
		return self.ovs

	def list_all(self):
		print "Not yet implemented"
		pass

	def sync(self, name):
		# check if we have a such overlay
		if not self.ovs.has_key(name):
			raise XovError("Overlay %s doesn't exist" % name)
		# build required env
		local_env = os.environ.copy()
		ov_env = self.ovs[name].get_env()
		# local_env['PORTDIR'] = ""
                if self.root:
                        ov_env['ROOT'] = self.root
                else:
                        ov_env['ROOT'] = ""
                # 2013-06-27: when passed by environment, variable are not expanded by portage
                # In normal case we have only to take care of ${ROOT}
		ov_env['PORTDIR'] = "%s/%s" % (self.ov_dir, name)
                ov_env['PORTDIR'] = re.sub('\${ROOT}', ov_env['ROOT'], ov_env['PORTDIR'])
                # don't ask for updating target profile in post_sync
                ov_env['NO_POSTSYNC']='1'
		ov_env['PORTDIR_OVERLAY'] = ""
		local_env.update(ov_env)
		ret = Popen(["emerge", "--sync"], bufsize = 0,
			stdout=self.stdout, stderr=self.stderr, shell=False,
			cwd=None, env=local_env).wait()
                if ret != 0:
                        raise XovError("emerge --sync failed")
		return ret

	def _read_config(self):
		ovs = self.config.read()
		self.ovs = ovs

	def _update_portage_config(self):
		cfg_file = self.cfg_dir + '/make.conf'
		if not os.path.isfile(cfg_file):
			raise XovError("%s doesn't exist" % cfg_file)
		fd = open(cfg_file, 'r+')
		ii = fd.readline()
		while ii != '':
			if self.xov_re.match(ii):
				return
			ii = fd.readline()
		# no sourcing of xov found, so we can add it
		print >> fd, 'source ./xov.conf'
		fd.close()

	def _write_config(self):
		self.config.write(self.ovs)
	


