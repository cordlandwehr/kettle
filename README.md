# Kettle

The start of a small meta-building tool that will allow
- configuration of build target platforms
- configuration of build steps for projects (e.g. env settings for CMake)
- janitor tasks like performing a clean build

## Local Configurations
Kettle ships a set of default build options for specific platforms, yet it does not provide build options for your specific projects. For those, you can put your local configurations into the subfilder local. There are two three types of configuration files:

- local/platform/*.cfg: such configurations override any configurations specified in conf/platform/*.cfg
- local/project/*.cfg: your local preject specific configurations
- local/environment.cfg: your local environment setup
- local/kettle.cfg: your local configurations for kettle



# Configuration Options
Note that Kettle combines several configuration files for a single project build.
Thereby, configuration files can override values from other files.

## Project Configuration
* Section "Environment":
** any "variable=value" element in this section is exported as environment value
* Section "Project"
** vcs: git (currently only option)
** vcsGitSubmodules: true/false, enables git submodule updates if vcs is Git
** vcsUrl: url to resository
** buildSystem: cmake (currently only option)
