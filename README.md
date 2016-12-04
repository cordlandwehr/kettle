# Kettle

Kettle is a build tool dedicated for complex multi platform projects that target
embedded devices. In such projects, one typically develops on a Linux host
machine, on which the project is also tested and debugged, and cross-compiles
for an embedded device, on which the project finally shall run. A project
thereby consists of several libraries, applications, and utilizes a meta build
system of its own (e.g., Yocto or Buildroot).

To support development in this area, Kettle provides the following functionality:
- same interface for building for the host system and the embedded device
  via a toolchain
- easy to share build configuration files
- configuration in a hiearchical system:
  global settings < platform specific settings < project specific settings
- reproducability of environment setups for every build
- janitor tasks like rebuilding

## Local Configurations
Kettle ships a set of default build options for specific platforms, yet it does
not provide build options for your specific projects. For those, you can put your
local configurations into the subfilder local. There are two three types of
configuration files:

- local/platform/*.cfg: such configurations override any configurations specified in conf/platform/*.cfg
- local/project/*.cfg: your local preject specific configurations
- local/environment.cfg: your local environment setup
- local/kettle.cfg: your local configurations for kettle

# Configuration Options
Note that Kettle combines several configuration files for a single project build.
Thereby, configuration files can override values from other files.

## Project Configuration

### Section "Environment"
* any "variable=value" element in this section is exported as environment value

### Section "Default
* makeArguments: any list of arguments to be appended to the make call (eg. "-j4")
* cmakeArguments: any list of arguments to be appended to the cmake call
* environmentScript: path to bash-script that sets environment variables (e.g. Yocto generated SDK environment setup script)

### Section "Project"
* vcs: git (currently only option)
* vcsGitSubmodules: true/false, enables git submodule updates if vcs is Git
* vcsUrl: url to resository
* buildSystem: cmake (currently only option)
