# Copyright (C) 2013, 2014 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.

import os
import unittest

from tests import utils

from virtinst import Capabilities
from virtinst import DomainCapabilities


conn = utils.open_testdefault()


class TestCapabilities(unittest.TestCase):
    def _buildCaps(self, filename):
        path = os.path.join("tests/capabilities-xml", filename)
        return Capabilities(conn, open(path).read())

    def testCapsCPUFeaturesOldSyntax(self):
        filename = "test-old-vmx.xml"
        host_feature_list = ["vmx"]

        caps = self._buildCaps(filename)
        for f in host_feature_list:
            self.assertEqual(caps.host.cpu.has_feature(f), True)

    def testCapsCPUFeaturesOldSyntaxSVM(self):
        filename = "test-old-svm.xml"
        host_feature_list = ["svm"]

        caps = self._buildCaps(filename)
        for f in host_feature_list:
            self.assertEqual(caps.host.cpu.has_feature(f), True)

    def testCapsCPUFeaturesNewSyntax(self):
        filename = "test-qemu-with-kvm.xml"
        host_feature_list = ['lahf_lm', 'xtpr', 'cx16', 'tm2', 'est', 'vmx',
            'ds_cpl', 'pbe', 'tm', 'ht', 'ss', 'acpi', 'ds']

        caps = self._buildCaps(filename)
        for f in host_feature_list:
            self.assertEqual(caps.host.cpu.has_feature(f), True)

        self.assertEqual(caps.host.cpu.model, "core2duo")
        self.assertEqual(caps.host.cpu.vendor, "Intel")
        self.assertEqual(caps.host.cpu.threads, 3)
        self.assertEqual(caps.host.cpu.cores, 5)
        self.assertEqual(caps.host.cpu.sockets, 7)

    def testCapsUtilFuncs(self):
        caps_with_kvm = self._buildCaps("test-qemu-with-kvm.xml")
        caps_no_kvm = self._buildCaps("test-qemu-no-kvm.xml")
        caps_empty = self._buildCaps("test-old-vmx.xml")

        def test_utils(caps, has_guests, is_kvm):
            if caps.guests:
                self.assertEqual(caps.guests[0].has_install_options(), has_guests)
                self.assertEqual(caps.guests[0].is_kvm_available(), is_kvm)

        test_utils(caps_empty, False, False)
        test_utils(caps_with_kvm, True, True)
        test_utils(caps_no_kvm, True, False)

    def testCapsNuma(self):
        cells = self._buildCaps("lxc.xml").host.topology.cells
        self.assertEqual(len(cells), 1)
        self.assertEqual(len(cells[0].cpus), 8)
        self.assertEqual(cells[0].cpus[3].id, '3')


    ####################################
    # Test getCPUModel output handling #
    ####################################

    def testCPUAPI(self):
        caps = self._buildCaps("test-qemu-with-kvm.xml")

        cpu_64 = caps.get_cpu_values("x86_64")
        cpu_32 = caps.get_cpu_values("i686")
        cpu_random = caps.get_cpu_values("mips")

        def test_cpu_map(cpumap, cpus):
            cpunames = sorted(cpumap, key=str.lower)

            for c in cpus:
                self.assertTrue(c in cpunames)

        self.assertEqual(cpu_64, cpu_32)

        x86_cpunames = [
            '486', 'athlon', 'Conroe', 'core2duo', 'coreduo', 'n270',
            'Nehalem', 'Opteron_G1', 'Opteron_G2', 'Opteron_G3', 'Penryn',
            'pentium', 'pentium2', 'pentium3', 'pentiumpro', 'phenom',
            'qemu32', 'qemu64']

        test_cpu_map(cpu_64, x86_cpunames)
        test_cpu_map(cpu_random, [])

        cpu_64 = caps.get_cpu_values("x86_64")
        self.assertTrue(len(cpu_64) > 0)


    ##############################
    # domcapabilities.py testing #
    ##############################

    def testDomainCapabilities(self):
        xml = open("tests/capabilities-xml/test-domcaps.xml").read()
        caps = DomainCapabilities(utils.open_testdriver(), xml)

        self.assertEqual(caps.os.loader.supported, True)
        self.assertEqual(caps.os.loader.get_values(),
            ["/foo/bar", "/tmp/my_path"])
        self.assertEqual(caps.os.loader.enum_names(), ["type", "readonly"])
        self.assertEqual(caps.os.loader.get_enum("type").get_values(),
            ["rom", "pflash"])


if __name__ == "__main__":
    unittest.main()
