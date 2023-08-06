# -*- coding: utf-8 -*-
#
# Main fork Pisi: Copyright (C) 2005 - 2011, Tubitak/UEKAE
#
# Copyright (C) 2016 - 2020, Suleyman POYRAZ (Zaryob)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# Inary Modules
import inary.context as ctx
from inary.util import colorize
from inary.util import join_path

# ActionsAPI Modules
from inary.actionsapi import error

# Standart Python Modules
import os
import grp
import pwd
import sys
import glob
import shutil
from inary.actionsapi.shelltools import can_access_file
import inary.actionsapi.autotools as autotools
import inary.actionsapi.cmaketools as cmaketools
import inary.actionsapi.mesontools as mesontools


# Gettext Library
import gettext
__trans = gettext.translation('inary', fallback=True)
_ = __trans.gettext


def configure(args=''):
    """Autobuilder setup"""
    if can_access_file("autogen.sh"):
        autotools.autogen(args)
    if can_access_file("configure"):
        autotools.configure(args)
    if can_access_file("meson.build"):
        mesontools.configure(args)
    if can_access_file("CmakeLists.txt"):
        cmaketools.configure(args)

def make(args=''):
    """Autobuilder build"""
    if can_access_file("autogen.sh"):
        autotools.make(args)
    if can_access_file("Makefile"):
        autotools.make(args)
    if can_access_file("meson.build"):
        mesontools.make(args)
    if can_access_file("CmakeLists.txt"):
        cmaketools.make(args)

def install(args=''):
    """Autobuilder install"""
    if can_access_file("autogen.sh"):
        autotools.install(args)
    if can_access_file("Makefile"):
        autotools.install(args)
    if can_access_file("meson.build"):
        mesontools.install(args)
    if can_access_file("CmakeLists.txt"):
        cmaketools.install(args)


setup=configure()
build=make()
