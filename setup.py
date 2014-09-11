#!/usr/bin/python
#
# Copyright (c) 2014 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.

import os
import subprocess

from setuptools import setup

from distutils import cmd, log
from distutils.command.install_data import install_data as _install_data
from distutils.command.build import build as _build


# Courtesy http://wiki.maemo.org/Internationalize_a_Python_application
class build_trans(cmd.Command):
    description = 'Compile .po files into .mo files'
    submodule_root = os.path.join(os.curdir, "subscription_manager")

    def initialize_options(self):
        self.build_base = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_base', 'build_base'))

    def compile(self, src, dest):
        log.info("Compiling %s" % src)
        cmd = ['msgfmt', '-c', '--statistics', '-o', dest, src]
        rc = subprocess.call(cmd)
        if rc != 0:
            raise RuntimeError("msgfmt failed for %s to %s" % (src, dest))

    def run(self):
        po_dir = os.path.join(build_trans.submodule_root, 'po')
        for path, names, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = f[:-3]
                    src = os.path.join(path, f)
                    dest_path = os.path.join(self.build_base, 'locale', lang, 'LC_MESSAGES')
                    dest = os.path.join(dest_path, 'sat5to6.mo')
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        self.compile(src, dest)
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            self.compile(src, dest)


class build(_build):
    sub_commands = _build.sub_commands + [('build_trans', None)]

    def run(self):
        _build.run(self)


class install_data(_install_data):
    def run(self):
        for lang in os.listdir('build/locale/'):
            lang_dir = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            lang_file = os.path.join('build', 'locale', lang, 'LC_MESSAGES', 'sat5to6.mo')
            self.data_files.append((lang_dir, [lang_file]))
        _install_data.run(self)

install_requires = []

test_require = [
      'mock',
      'nose',
      'coverage',
      'polib',
      'pep8',
      'pyflakes',
    ] + install_requires

cmdclass = {
    'build': build,
    'build_trans': build_trans,
    'install_data': install_data,
}

setup(name="sat5to6",
      version='1.0.0',
      url="http://www.candlepinproject.org",
      description="Migrate Satellite 5 systems to Satellite 6.",
      license="GPLv2",
      author="Alex Wood",
      author_email="awood@redhat.com",
      cmdclass=cmdclass,
      packages=[
          'sat5to6',
          ],
      package_dir={
          'sat5to6': 'subscription_manager/src/subscription_manager/migrate',
       },
      data_files=[
          ('sbin', ['subscription_manager/bin/sat5to6']),
      ],
      include_package_data=True,
      install_requires=install_requires,
      test_suite='nose.collector',
      tests_require=test_require
    )
