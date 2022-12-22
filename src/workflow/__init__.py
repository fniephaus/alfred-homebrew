#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2022 Thomas Harr <xDevThomas@gmail.com>
# Copyright (c) 2019 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-02-15
#

"""A helper library for `Alfred <http://www.alfredapp.com/>`_ workflows."""

import os

# Icons, Filter matching rules, Exceptions and Workflow objects
from workflow.workflow import (ICON_ACCOUNT, ICON_BURN, ICON_CLOCK, ICON_COLOR,
                               ICON_COLOUR, ICON_EJECT, ICON_ERROR,
                               ICON_FAVORITE, ICON_FAVOURITE, ICON_GROUP,
                               ICON_HELP, ICON_HOME, ICON_INFO, ICON_NETWORK,
                               ICON_NOTE, ICON_SETTINGS, ICON_SWIRL,
                               ICON_SWITCH, ICON_SYNC, ICON_TRASH, ICON_USER,
                               ICON_WARNING, ICON_WEB, MATCH_ALL,
                               MATCH_ALLCHARS, MATCH_ATOM, MATCH_CAPITALS,
                               MATCH_INITIALS, MATCH_INITIALS_CONTAIN,
                               MATCH_INITIALS_STARTSWITH, MATCH_STARTSWITH,
                               MATCH_SUBSTRING, KeychainError,
                               PasswordNotFound, Variables, Workflow, manager)

__title__ = 'Alfred-PyWorkflow'
__version__ = open(os.path.join(os.path.dirname(__file__), 'version')).read()
__author__ = 'Thomas Harr, Dean Jackson'
__licence__ = 'MIT'
__copyright__ = 'Copyright 2022 Thomas Harr, Copyright 2014-2019 Dean Jackson'

__all__ = [
    'Variables',
    'Workflow',
    'manager',
    'PasswordNotFound',
    'KeychainError',
    'ICON_ACCOUNT',
    'ICON_BURN',
    'ICON_CLOCK',
    'ICON_COLOR',
    'ICON_COLOUR',
    'ICON_EJECT',
    'ICON_ERROR',
    'ICON_FAVORITE',
    'ICON_FAVOURITE',
    'ICON_GROUP',
    'ICON_HELP',
    'ICON_HOME',
    'ICON_INFO',
    'ICON_NETWORK',
    'ICON_NOTE',
    'ICON_SETTINGS',
    'ICON_SWIRL',
    'ICON_SWITCH',
    'ICON_SYNC',
    'ICON_TRASH',
    'ICON_USER',
    'ICON_WARNING',
    'ICON_WEB',
    'MATCH_ALL',
    'MATCH_ALLCHARS',
    'MATCH_ATOM',
    'MATCH_CAPITALS',
    'MATCH_INITIALS',
    'MATCH_INITIALS_CONTAIN',
    'MATCH_INITIALS_STARTSWITH',
    'MATCH_STARTSWITH',
    'MATCH_SUBSTRING',
]
