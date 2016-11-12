# Copyright 2016  Andreas Cord-Landwehr <cordlandwehr@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#!/usr/bin/python
import sys
import argparse
from symbol import argument
from kettlelib import *

# command line arguments
parser = argparse.ArgumentParser(description='Semi-automatic build tool for triggering project builds')
parser.add_argument('--project', type=str)
parser.add_argument('--platform', type=str, default='linux')
parser.add_argument('--compiler', type=str, choices=['gcc', 'clang'], default='gcc')
arguments = parser.parse_args( )

# initial status information
print(PrintColors.Header + "Kettle Multi-Platform Building" + PrintColors.End)
print("project:  " + PrintColors.Bold + arguments.project + PrintColors.End)
print("platform: " + PrintColors.Bold + arguments.platform + PrintColors.End + "\n")

# initializing manager prints environment
manager = BuildManager(arguments.project, arguments.platform)

# Update sources
print(PrintColors.Header + "## Update Project Sources" + PrintColors.End)
if not manager.update_sources():
    sys.exit("Configuration exited with non-zero code, assuming failure to configure for project %s." % arguments.project)
print()

# Configure the build system configuration
print(PrintColors.Header + "## Configuring Build" + PrintColors.End)
if not manager.configure_build():
    sys.exit("Configuration exited with non-zero code, assuming failure to configure for project %s." % arguments.project)
print()

# Perform the build
print(PrintColors.Header + "## Perform Build" + PrintColors.End)
if not manager.perform_build():
    sys.exit("Building exited with non-zero code, assuming failure to build the project %s." % arguments.project)
print()

# Perform the install step
print(PrintColors.Header + "## Perform Install" + PrintColors.End)
if not manager.perform_install():
    sys.exit("Building exited with non-zero code, assuming failure to install the project %s." % arguments.project)
