# Copyright (C) 2016 Red Hat, Inc.
# Copyright (C) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Charles Arnold <carnold suse com>
#
# This work is licensed under the GNU GPLv2.
# See the COPYING file in the top-level directory.
import datetime

from ..xmlbuilder import XMLBuilder, XMLProperty


class DomainSysinfo(XMLBuilder):
    """
    Class for building and domain <sysinfo> XML
    """

    XML_NAME = "sysinfo"
    _XML_PROP_ORDER = ["type",
        "bios_vendor", "bios_version", "bios_date", "bios_release",
        "system_manufacturer", "system_product", "system_version",
        "system_serial", "system_uuid", "system_sku", "system_family",
        "baseBoard_manufacturer", "baseBoard_product", "baseBoard_version",
        "baseBoard_serial", "baseBoard_asset", "baseBoard_location"]

    type = XMLProperty("./@type")

    def _validate_date(self, val):
        # If supplied, date must be in either mm/dd/yy or mm/dd/yyyy format
        try:
            datetime.datetime.strptime(val, '%m/%d/%Y')
        except ValueError:
            try:
                datetime.datetime.strptime(val, '%m/%d/%y')
            except ValueError:
                raise RuntimeError(_("SMBios date string '%s' is invalid.")
                            % val)
        return val

    bios_date = XMLProperty("./bios/entry[@name='date']",
                            validate_cb=_validate_date)
    bios_vendor = XMLProperty("./bios/entry[@name='vendor']")
    bios_version = XMLProperty("./bios/entry[@name='version']")
    bios_release = XMLProperty("./bios/entry[@name='release']")

    system_uuid = XMLProperty("./system/entry[@name='uuid']")
    system_manufacturer = XMLProperty("./system/entry[@name='manufacturer']")
    system_product = XMLProperty("./system/entry[@name='product']")
    system_version = XMLProperty("./system/entry[@name='version']")
    system_serial = XMLProperty("./system/entry[@name='serial']")
    system_sku = XMLProperty("./system/entry[@name='sku']")
    system_family = XMLProperty("./system/entry[@name='family']")

    baseBoard_manufacturer = XMLProperty(
        "./baseBoard/entry[@name='manufacturer']")
    baseBoard_product = XMLProperty("./baseBoard/entry[@name='product']")
    baseBoard_version = XMLProperty("./baseBoard/entry[@name='version']")
    baseBoard_serial = XMLProperty("./baseBoard/entry[@name='serial']")
    baseBoard_asset = XMLProperty("./baseBoard/entry[@name='asset']")
    baseBoard_location = XMLProperty("./baseBoard/entry[@name='location']")
