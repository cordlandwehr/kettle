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

import configparser
import multiprocessing
import os
import subprocess
import sys

class BuildManager(object):
    # Make sure we have our configuration and the project we are building available
    def __init__(self, project, platform):
        # save them for later use
        self.project = project
        self.platform = platform
        # TODO add configuration
        self.buildDirectory = os.path.join("build", self.project)
        self.sourceDirectory = os.path.abspath( os.path.join("source", self.project) )
        self.environment = self.generate_environment()

        print("== Build Environment")
        for name, value in self.environment.items():
            print("export " + name + "=" + value)

    def generate_environment(self):
        """Generate and return configuration and build environment"""

        # these values are loaded from the system and optionally prefixed from configuration files
        systemEnvVariables = [
            'CMAKE_PREFIX_PATH', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'PATH', 'LD_LIBRARY_PATH', 'PKG_CONFIG_PATH', 'PYTHONPATH',
            'PERL5LIB', 'QT_PLUGIN_PATH', 'QML_IMPORT_PATH', 'QML2_IMPORT_PATH', 'QMAKEFEATURES', 'PYTHON3PATH', 'CPLUS_INCLUDE_PATH'
        ]
        environment = {}
        for var in systemEnvVariables:
            environment[var] = os.getenv(var, "")

        # update environment with
        envConfig = configparser.SafeConfigParser()
        envConfig.read(['config/platform/' + self.platform + '.cfg', 'environment.cfg'])
        for var, value in envConfig.items("Default"):
            if var in environment:
                environment[var] = value + ":" + environment[var]
            else:
                environment[var] = value
        return environment

    def configure_build(self):
        """Calls the met-build system (e.g. CMake) to generate the Makefiles"""

        # determine the directory we will perform the build in and make sure it exists
        buildDirectory = self.buildDirectory
        if not os.path.exists( buildDirectory ):
            os.makedirs( buildDirectory )

        #TODO hardcoded: read it from configuration files
        configureCommand = [ 'cmake' ]
        configureCommand.append( self.sourceDirectory )

        try:
            print(configureCommand)
            process = subprocess.check_call(configureCommand, stdout=sys.stdout, stderr=sys.stderr, cwd=buildDirectory, env=self.environment)
        except subprocess.CalledProcessError:
            # Abort if it fails to complete
            return False
        return True

    def perform_build(self):
        """Calls make to perform the actual build"""

        # build directory must exist after configuration
        buildDirectory = self.buildDirectory
        buildCommand = [ 'make' ]
        try:
            print(buildCommand)
            process = subprocess.check_call(buildCommand, stdout=sys.stdout, stderr=sys.stderr, cwd=buildDirectory, env=self.environment)
        except subprocess.CalledProcessError:
            # Abort if it fails to complete
            return False
        return True
