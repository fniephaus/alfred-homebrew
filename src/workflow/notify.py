#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2022 Thomas Harr <xDevThomas@gmail.com>
# Copyright (c) 2019 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2015-11-26
#

"""
Post notifications via the macOS Notification Center.

This feature is only available on Mountain Lion (10.8) and later.
It will silently fail on older systems.

The main API is a single function, :func:`~workflow.notify.notify`.

It works by creating a simple application to your workflow's cache
directory. It replaces the application's icon with your workflow's
icon and then calls the application to post notifications. The app
is rebuilt if it is over a month old at the time of the notification,
to refresh outdated icons.

This module uses ``Notificator`` logic created by Vítor Galvão
 https://github.com/vitorgalvao/notificator
"""

import os
import plistlib
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import timedelta

import workflow

_wf = None
_log = None


#: Available system sounds from System Preferences > Sound > Sound Effects
# (location: ``/System/Library/Sounds``)
SOUNDS = (
    'Basso',
    'Blow',
    'Bottle',
    'Frog',
    'Funk',
    'Glass',
    'Hero',
    'Morse',
    'Ping',
    'Pop',
    'Purr',
    'Sosumi',
    'Submarine',
    'Tink',
)


def wf():
    """Return Workflow object for this module.

    Returns:
        workflow.Workflow: Workflow object for current workflow.
    """
    global _wf
    if _wf is None:
        _wf = workflow.Workflow()
    return _wf


def log():
    """Return logger for this module.

    Returns:
        logging.Logger: Logger for this module.
    """
    global _log
    if _log is None:
        _log = wf().logger
    return _log

def notificator_name():
    """Notificator name from Alfred's workflow name.
    ``Notificator for `~workflow.name`.app``

        :returns: notificator name
        :rtype: ``str``

        """
    return f'Notificator for {wf().name}.app'


def notificator_program():
    """Return path to Notificator applet executable.

    Returns:
        str: Path to ``Notificator for `~workflow.name`.app`` ``applet`` executable.
    """
    return wf().cachefile(f'{notificator_name()}/Contents/MacOS/applet')


def notificator_icon_path():
    """Return path to icon file in installed ``Notificator for `~workflow.name`.app``.

    Returns:
        str: Path to ``applet.icns`` within the app bundle.
    """
    return wf().cachefile(f'{notificator_name()}/Contents/Resources/applet.icns')


def install_notificator():
    """Build the ``Notificator for `~workflow.name`.app`` from the workflow to cache directory.

    Changes the bundle ID of the installed app and gives it the
    workflow's icon.
    """
    jxa_script='''
    // Build argv/argc in a way that can be used from the applet inside the app bundle
    ObjC.import("Foundation")
    const args = $.NSProcessInfo.processInfo.arguments
    const argv = []
    const argc = args.count
    for (let i = 0; i < argc; i++) { argv.push(ObjC.unwrap(args.objectAtIndex(i))) }
    // Notification script
    const app = Application.currentApplication()
    app.includeStandardAdditions = true
    if (argv.length < 2) { // We use "2" because the script will always see at least one argument: the applet itself
        argv[1] = "Opening usage instructions…"
        argv[2] = "Notificator is a command-line app"
        argv[4] = "Funk"
        app.openLocation("https://github.com/vitorgalvao/notificator#usage")
    }
    const message = argv[1]
    const title = argv[2]
    const subtitle = argv[3]
    const sound = argv[4]
    const options = {}
    if (title) options.withTitle = title
    if (subtitle) options.subtitle = subtitle
    if (sound) options.soundName = sound
    app.displayNotification(message, options)
    '''
    destdir = wf().cachedir
    app_name = notificator_name()
    app_path = os.path.join(destdir, app_name)

    log().debug(f'installing "{app_name}" to {destdir} ...')

    cmd = [
        'osacompile',
        '-l', 'JavaScript',
        '-o', app_path,
        '-e', jxa_script
        ]
    retcode = subprocess.call(cmd)
    if retcode != 0: # pragma: nocover
        raise RuntimeError(f'oscompile exited with {retcode}')

    n = notificator_program()
    if not os.path.exists(n): # pragma: nocover
        raise RuntimeError(f'{app_name} could not be installed in ' + destdir)

    # Replace applet icon
    icon = notificator_icon_path()
    workflow_icon = wf().workflowfile('icon.png')
    if os.path.exists(icon):
        os.unlink(icon)

    png_to_icns(workflow_icon, icon)

    # Modify Notificator, change bundle ID of installed app
    ip_path = os.path.join(app_path, 'Contents/Info.plist')
    #bundle_id = f'{wf().bundleid}.{uuid.uuid4().hex}'
    bundle_id = f'{wf().bundleid}'
    with open(ip_path, 'rb') as fp:
        data = plistlib.load(fp)
    log().debug('changing bundle ID to %r', bundle_id)
    data['CFBundleIdentifier'] = bundle_id
    data['LSUIElement'] = '1'
    with open(ip_path, 'wb') as fp:
        plistlib.dump(data, fp)

    # Redo signature
    cmd = [
        'codesign',
        '--remove-signature', app_path
    ]
    retcode = subprocess.call(cmd)
    if retcode != 0: # pragma: nocover
        raise RuntimeError(f'codesign remove-signature exited with {retcode}')

    cmd = [
        'codesign',
        '--sign', '-', app_path
    ]
    retcode = subprocess.call(cmd)
    if retcode != 0: # pragma: nocover
        raise RuntimeError(f'codesign sign exited with {retcode}')


def validate_sound(sound):
    """Coerce ``sound`` to valid sound name.

    Returns ``None`` for invalid sounds. Sound names can be found
    in ``System Preferences > Sound > Sound Effects`` or located at ``/System/Library/Sounds``.

    Args:
        sound (str): Name of system sound.

    Returns:
        str: Proper name of sound or ``None``.
    """
    if not sound:
        return None

    # Case-insensitive comparison of `sound`
    if sound.lower() in [s.lower() for s in SOUNDS]:
        # Title-case is correct for all system sounds as of macOS 10.11
        return sound.title()
    return None


def notify(title='', subtitle='', message='', sound=None):
    """Post notification via notificator helper app  from Vítor Galvão.

    Args:
        title (str, optional): Notification title.
        subtitle (str, optional): Notification title.
        message (str): Notification body text.
        sound (str, optional): Name of sound to play.

    Raises:
        ValueError: Raised if both ``title`` and ``text`` are empty.

    Returns:
        bool: ``True`` if notification was posted, else ``False``.
    """
    if message == '':
        raise ValueError('Empty notification message')

    sound = validate_sound(sound) or ''

    n = notificator_program()

    # Install if Notificator does not exist or was modified more than 30 days ago
    if (not os.path.exists(n)) or timedelta(seconds=time.time() - os.path.getmtime(n)).days >= 30:
        install_notificator()

    cmd = [
        n,
        message,
        title,
        subtitle,
        sound
        ]
    retcode = subprocess.call(cmd)
    if retcode == 0:
        return True

    log().error('Notify.app exited with status {0}.'.format(retcode))
    return False


def convert_image(inpath, outpath, size):
    """Convert an image file using ``sips``.

    Args:
        inpath (str): Path of source file.
        outpath (str): Path to destination file.
        size (int): Width and height of destination image in pixels.

    Raises:
        RuntimeError: Raised if ``sips`` exits with non-zero status.
    """
    cmd = [
        'sips',
        '--resampleHeightWidth', str(size), str(size),
        inpath,
        '--out', outpath]
    # log().debug(cmd)
    with open(os.devnull, 'w') as pipe:
        retcode = subprocess.call(cmd, stdout=pipe, stderr=subprocess.STDOUT)

    if retcode != 0:
        raise RuntimeError('sips exited with %d' % retcode)


def png_to_icns(png_path, icns_path):
    """Convert PNG file to ICNS using ``iconutil``.

    Create an iconset from the source PNG file. Generate PNG files
    in each size required by macOS, then call ``iconutil`` to turn
    them into a single ICNS file.

    Args:
        png_path (str): Path to source PNG file.
        icns_path (str): Path to destination ICNS file.

    Raises:
        RuntimeError: Raised if ``iconutil`` or ``sips`` fail.
    """
    tempdir = tempfile.mkdtemp(prefix='aw-', dir=wf().cachedir)

    try:
        iconset = os.path.join(tempdir, 'icon.iconset')

        if os.path.exists(iconset):  # pragma: nocover
            raise RuntimeError('iconset already exists: ' + iconset)

        os.makedirs(iconset)

        # Copy source icon to icon set and generate all the other
        # sizes needed
        configs = []
        for i in (16, 32, 64, 128, 256, 512):
            configs.append((f'icon_{i}x{i}.png', i))
            configs.append(((f'icon_{i}x{i}@2x.png', i * 2)))

        for name, size in configs:
            outpath = os.path.join(iconset, name)
            if os.path.exists(outpath): # pragma: nocover
                continue
            convert_image(png_path, outpath, size)

        cmd = [
            'iconutil',
            '--convert', 'icns',
            '--output', icns_path,
            iconset]

        retcode = subprocess.call(cmd)
        if retcode != 0:
            raise RuntimeError(f'iconset exited with {retcode}')

        if not os.path.exists(icns_path):  # pragma: nocover
            raise ValueError(f'generated ICNS file not found: {icns_path}')
    finally:
        try:
            shutil.rmtree(tempdir)
        except OSError:  # pragma: no cover
            pass


if __name__ == '__main__':  # pragma: nocover
    # Simple command-line script to test module with
    # This won't work on 2.6, as `argparse` isn't available
    # by default.
    import argparse
    from unicodedata import normalize

    def ustr(s):
        """Coerce `s` to normalised Unicode."""
        return normalize('NFD', s.decode('utf-8'))

    p = argparse.ArgumentParser()
    p.add_argument('-p', '--png', help="PNG image to convert to ICNS.")
    p.add_argument('-l', '--list-sounds', help="Show available sounds.",
                   action='store_true')
    p.add_argument('-t', '--title',
                   help="Notification title.", type=ustr,
                   default='')
    p.add_argument('-s', '--sound', type=ustr,
                   help="Optional notification sound.", default='')
    p.add_argument('text', type=ustr,
                   help="Notification body text.", default='', nargs='?')
    o = p.parse_args()

    # List available sounds
    if o.list_sounds:
        for sound in SOUNDS:
            print(sound)
        sys.exit(0)

    # Convert PNG to ICNS
    if o.png:
        icns = os.path.join(
            os.path.dirname(o.png),
            os.path.splitext(os.path.basename(o.png))[0] + '.icns')

        print('converting {0!r} to {1!r} ...'.format(o.png, icns),
              file=sys.stderr)

        if os.path.exists(icns):
            raise ValueError('destination file already exists: ' + icns)

        png_to_icns(o.png, icns)
        sys.exit(0)

    # Post notification
    if o.title == o.text == '':
        print('ERROR: empty notification.', file=sys.stderr)
        sys.exit(1)
    else:
        notify(o.title, o.text, o.sound)
