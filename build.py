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

manager = BuildManager(arguments.project, arguments.platform)

# initial status information
print("\nKettle Tool starting...")
print("== Building Project: %s" %(arguments.project))

# Update sources
print("\n== Update Project Sources\n")
if not manager.update_sources():
    sys.exit("Configuration exited with non-zero code, assuming failure to configure for project %s." % arguments.project)

# Configure the build
print("\n== Configuring Build\n")
if not manager.configure_build():
    sys.exit("Configuration exited with non-zero code, assuming failure to configure for project %s." % arguments.project)

# Perform the build
print("\n== Perform Build\n")
if not manager.perform_build():
    sys.exit("Building exited with non-zero code, assuming failure to build the project %s." % arguments.project)
