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

        # generate build environment
        self.buildDirectory = os.path.join("build", self.project)
        self.sourceDirectory = os.path.abspath( os.path.join("source", self.project) )
        self.environment = self.generate_environment()
        print("== Build Environment: " + self.project)
        for name, value in self.environment.items():
            print("export " + name + "=" + value)

        # read project configuration
        print("== Parsing Project Configuration ")
        projectConfig = configparser.SafeConfigParser()
        projectConfig.read(['local/project/' + self.project + '.cfg', 'local/project/' + self.project + '.cfg'])
        # get VCS system
        if not projectConfig.has_option('Project', 'vcs'):
            self.projectVcs = 'git'
            print('- \"vcs\" key missing: falling back to \"git\"')
        else:
            self.projectVcs = projectConfig.get('Project', 'vcs')
        # get optional VCS URL
        if not projectConfig.has_option('Project', 'vcsUrl'):
            self.projectVcsUrl = ''
            print('- \"vcsUrl\" key missing: will not be able to update or checkout source code')
        else:
            self.projectVcsUrl = projectConfig.get('Project', 'vcsUrl')
        # get build system (CMake for QMake)
        if not projectConfig.has_option('Project', 'buildSystem'):
            self.projectBuildSystem = ''
            print('- \"buildSystem\" key missing: cannot perform build')
        else:
            self.projectBuildSystem = projectConfig.get('Project', 'buildSystem')
        return

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
        envConfig.read(['config/platform/' + self.platform + '.cfg', 'local/platform' + self.platform, 'environment.cfg'])
        for var, value in envConfig.items("Default"):
            if var in environment:
                environment[var] = value + ":" + environment[var]
            else:
                environment[var] = value
        return environment

    def update_sources(self):
        """Initialize source control system or update sources if already checked out"""

        if not self.projectVcs == "git":
            print("VCS system different to git, aborting since git is only supported system right now")
            return False

        if not os.path.exists(self.buildDirectory) and self.projectVcsUrl != '':
            try:
                print("checking out to: " + self.sourceDirectory)
                process = subprocess.check_call(["git", "clone", self.projectVcsUrl] + self.sourceDirectory, stdout=sys.stdout, stderr=sys.stderr, cwd=buildDirectory)
            except subprocess.CalledProcessError:
                # Abort if it fails to complete
                return False
        else:
            try:
                print("updating sources in: " + self.sourceDirectory)
                process = subprocess.check_call(["git", "pull"], stdout=sys.stdout, stderr=sys.stderr, cwd=self.sourceDirectory)
            except subprocess.CalledProcessError:
                # Abort if it fails to complete
                return False
        return True

    def configure_build(self):
        """Calls the meta-build system (e.g. CMake) to generate the Makefiles"""

        # determine the directory we will perform the build in and make sure it exists
        buildDirectory = self.buildDirectory
        if not os.path.exists( buildDirectory ):
            os.makedirs( buildDirectory )

        #read "cmake" or "qmake" value from config
        configureCommand = [self.projectBuildSystem]
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
