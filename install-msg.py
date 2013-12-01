#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MSG Install Script

This is an interface to the install process.

1. Create the distribution archive.
2. Extract the distribution archive.
2. Install the distribution from the current code base.

Usage:

    python install-msg.py --sourcePath ${ROOT_PATH_TO_SOURCE}
    --installPathUser ${BASE_PATH_OF_USER_BASED_INSTALL}

The distribution archive is placed in ${ROOT_PATH_TO_SOURCE}/dist.

The software is installed to path given by the base path to a directory named
after the software including its version number.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import subprocess
import argparse
import os
from msg_logger import MSGLogger
import pkg_resources
import tarfile


def processCommandLineArguments():
    global argParser, commandLineArgs
    argParser = argparse.ArgumentParser(description = '')
    argParser.add_argument('--sourcePath',
                           help = 'Path where the source code is located.',
                           required = True)
    argParser.add_argument('--installPathUser',
                           help = 'Path to be used for a user based install.',
                           required = True)

    commandLineArgs = argParser.parse_args()


def runCommand(cmd = None):
    if cmd is not None:
        try:
            subprocess.check_call(cmd, shell = True)
        except subprocess.CalledProcessError, e:
            logger.log("An exception occurred: %s" % e, 'error')


def softwareInstallName():
    cmd = "python %s/setup.py --name" % commandLineArgs.sourcePath
    try:
        softwareName = subprocess.check_output(cmd, shell = True)
    except subprocess.CalledProcessError, e:
        logger.log("An exception occurred: %s" % e, 'error')
    return softwareName.strip()


def softwareVersion():
    """
    There may be issues with retrieving the version number this way when
    dependencies are defined in __init.py__.
    """

    cmd = "python %s/setup.py --version" % commandLineArgs.sourcePath
    try:
        softwareVersion = subprocess.check_output(cmd, shell = True)
    except subprocess.CalledProcessError, e:
        logger.log("An exception occurred: %s" % e, 'error')
    return softwareVersion.strip()


commandLineArgs = None
logger = MSGLogger(__name__)
processCommandLineArguments()

os.chdir(commandLineArgs.sourcePath)

print "%s" % os.getcwd()

archiveCmd = """python setup.py sdist"""
runCommand(archiveCmd)

PROJECT_NAME = softwareInstallName()
VERSION = softwareVersion()

print "Performing scripted install of %s-%s." % (PROJECT_NAME, VERSION)

installCmd = """python setup.py install --home=%s""" % commandLineArgs\
    .installPathUser
runCommand(installCmd)

# Extract the distribution archive.
tarfile.open(name = '%s/dist/%s-%s.tar.gz' % (
commandLineArgs.sourcePath, PROJECT_NAME, VERSION))

print "\nInstallation of the MSG software to %s is complete." % \
      commandLineArgs.installPathUser
print "\nPlease add the following path, %s/lib/python, to your PYTHONPATH if " \
      "it " \
      "is not already there." % commandLineArgs.installPathUser
