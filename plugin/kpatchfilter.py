#
# Copyright (C) 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

import dnf
import hawkey

class KpatchFilter(dnf.Plugin):

    name = 'kpatchfilter'
    # list of package names to filter based on kpatch support
    kernel_pkg_names = ['kernel', 'kernel-core', 'kernel-modules', 'kernel-modules-core', 'kernel-modules-extra']

    def __init__(self, base, cli):
        super(KpatchFilter, self).__init__(base, cli)
        self.base = base

    def config(self):
        # Read the plugin config file. Currently it does not recognize any config options
        pass

    def sack(self):
        # This query gradually accumulates all kernel packages that should be
        # offered to the user (kernels for which exists kpatch-patch-* package
        # that requires it). Start with empty query.
        kernels_keep = self.base.sack.query().filterm(empty=True)

        # pre-filter all available versions of the kernel* packages
        kernels_query = self.base.sack.query(flags=hawkey.IGNORE_EXCLUDES)
        kernels_query.filterm(name=self.kernel_pkg_names)
        # any installed kernel version should not be excluded
        kernels_query = kernels_query.available()

        # Add to the kernels_keep query all kernel-core package versions that are
        # required by any of kpatch-patch-* packages.
        kpatch_query = self.base.sack.query(flags=hawkey.IGNORE_EXCLUDES)
        kpatch_query.filterm(name__glob="kpatch-patch-*")
        for kpatch_pkg in kpatch_query:
            for require in kpatch_pkg.requires:
                if require.name == "kernel-uname-r":
                    # get kernel-core package providing "kernel-uname-r = <kpatch_pkg.evra>"
                    kernel_core = kernels_query.filter(provides=require)
                    kernel_evr = None
                    for kernel_core_pkg in kernel_core:
                        # assume that all such packages have the same evr
                        kernel_evr = kernel_core_pkg.evr
                        break
                    if kernel_evr is not None:
                        kernels_keep = kernels_keep.union(kernels_query.filter(evr=kernel_evr))
                    # assume the is only one kernel-uname-r requirement
                    break

        # exclude all kernel-core packages that are not in kernels_keep query
        self.base.sack.add_excludes(kernels_query.difference(kernels_keep))
