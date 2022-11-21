#!/usr/bin/env python3

import argparse
import os
import pathlib
import shutil
import subprocess
import sys

class NuGetCli(object) :

    #
    # Description
    #   The class constructor
    #
    # Parameters
    #   mono  - The path to mono executable (None if not found)
    #   nuget - The path to the nuget executable
    #
    def __init__(self, mono, nuget, verbose) :
        self.mono = mono
        self.nuget = nuget
        self.verbose = verbose

    #
    # Description
    #   This function creates the base command
    #   to call (i.e. nuget or mono nuget)
    #
    # Parameters
    #   None
    #
    # Returns
    #   [ nuget ] or [ mono nuget ]
    #
    def get_base_cmd(self) :

        if self.mono :
            return [ self.mono, self.nuget ]

        return [ self.nuget ]

    #
    # Description
    #   This function manipulates nuget sources
    #
    #   see https://docs.microsoft.com/en-us/nuget/reference/cli-reference/cli-ref-sources
    #   for documentation
    #
    # Parameters
    #   action  - The action (add, remove, update, etc, ...)
    #   name    - The repository user friendly name
    #   url     - The repository url
    #   user    - The Artifactory user
    #   api_key - The API key of this user
    #
    # Returns
    #   The result of the command.
    #
    # Exceptions
    #   throw subprocess.CalledProcessError in case of error
    #
    def sources(self, action, name, url, user, api_key, password_in_clear) :

        cmd = self.get_base_cmd()
        cmd.extend([ "sources", action, "-Name", name, "-Source", url, "-username", user, "-password", api_key])

        if password_in_clear :
            cmd.append("-StorePasswordInClearText")

        return self.run(cmd)

    #
    # Description
    #   This function manipulates nuget set API key
    #
    #   see https://docs.microsoft.com/en-us/nuget/reference/cli-reference/cli-ref-setapikey
    #   for documentation
    #
    # Parameters
    #   name    - The repository user friendly name
    #   user    - The Artifactory user
    #   api_key - The API key of this user
    #
    # Returns
    #   The result of the command.
    #
    # Exceptions
    #   throw subprocess.CalledProcessError in case of error
    #
    def setapikey(self, name, user, api_key) :

        cmd = self.get_base_cmd()
        cmd.extend([ "setapikey", "{}:{}".format(user, api_key), "-source", name ])
        #cmd.extend(["setapikey", api_key, "-source", name])

        return self.run(cmd)

    #
    # Description
    #   This function executes the given command
    #
    # Parameters
    #   cmd - The command
    #
    # Returns
    #   The result of the command.
    #
    # Exceptions
    #   throw subprocess.CalledProcessError in case of error
    #
    def run(self, cmd) :

        if self.verbose :
            print("[cmd] >> {}".format(cmd))

        return subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#
# Description
#   This is the entry point of the script
#
# Parameters
#   argv - The arguments passed on the command line
#
# Returns
#   0 - The operation was successful
#  !0 - The operation failed
#
def main(argv):

    parser = argparse.ArgumentParser(description="This script creates the NuGet configuration file to enable vcpkg binary caching with Artifactory")

    # Mandatory arguments
    requiredArguments = parser.add_argument_group('Mandatory arguments')

    requiredArguments.add_argument("--name",       dest="name",     help="The name to identify this repository")
    requiredArguments.add_argument("--api-key",    dest="api_key",  help="The Artifactory API key")
    requiredArguments.add_argument("--url",        dest="url",      help="The Artifactory repository URL")
    requiredArguments.add_argument("--user",       dest="user",     help="The Artifactory user")

    # Optional arguments
    parser.add_argument("--vcpkg-root",         dest="vcpkg_root",         help="The path to your vpckg root directory")
    parser.add_argument("--delete-file-before", dest="delete_file_before", help="Delete the NuGet.Config file before adding the repository", action="store_true")
    parser.add_argument("--verbose",            dest="verbose",            help="Print all command submitted", action="store_true")
    parser.add_argument("--password-in-clear",  dest="password_in_clear",  help="Store the password in clear", action="store_true")

    args = parser.parse_args(argv)

    verbose = args.verbose

    #========================
    #== Check NuGet.Config ==
    #========================

    # There might be cases where we will want to wipe
    # the configuration file completely. By default,
    # we do nothing and simply display if we found the
    # configuration file at the place we expect it to be

    if "APPDATA" in os.environ :
        nuget_config_file = os.path.join(os.environ["APPDATA"], "NuGet", "NuGet.Config")
    else :
        nuget_config_file = os.path.join(os.environ["HOME"], ".config", "NuGet", "NuGet.Config")

    if os.path.isfile(nuget_config_file) :
        print("-- NuGet.Config found at {}".format(nuget_config_file))
    else :
        print("-- NuGet.Config expected at {}".format(nuget_config_file))

    if args.delete_file_before and os.path.isfile(nuget_config_file) :
        try :
            print("-- Deleting NuGet.Config at {}".format(nuget_config_file))
            os.remove(nuget_config_file)
        except OSError as e :
            print ("-- Error: {} - {}".format(e.filename, e.strerror))
            raise


    # Objectives
    #  We are going to set a repository to serve
    #  as a binary cache for vcpkg. As such, it's
    #  worth it to
    #    1°) Check that vcpkg is properly configured (i.e. vcpkg executable exists)
    #    2°) Get the nuget.exe that vcpkg is going to use (vpckg fetch nuget)
    #        - For portability under Linux, check if mono is installed
    #    3°) Use nuget.exe itself to configure our repository

    #===============
    #== GET VCPKG ==
    #===============

    if args.vcpkg_root :
        vcpkg_root = args.vcpkg_root
    elif "VCPKG_ROOT" in os.environ :
        vcpkg_root = os.environ["VCPKG_ROOT"]
    else :
        raise ValueError("You did not specify where vcpkg root is located\n"
                         "This can be done either through --vcpkg-root option or"
                         " VCPKG_ROOT environment variable")

    # Check that vcpkg can be found
    vcpkg = shutil.which("vcpkg", path=vcpkg_root)

    if not vcpkg :
        raise RuntimeError("No vcpkg executable found at {}. Is vcpkg bootstrapped ?".format(vcpkg_root))

    #===============
    #== Get nuget ==
    #===============

    # NuGet requires mono under linux
    mono = shutil.which("mono")

    # Display a warning if not found. Probably suspicious
    if not mono and sys.platform == "linux" :
        print("WARNING : It seems you are on Linux machine and mono was not found."
              " mono is required in order for NuGet to work")

    # If nuget is not yet downloaded this command might fail
    for i in range(0, 2) :
        result = subprocess.run([vcpkg, "fetch", "nuget"], stdout=subprocess.PIPE, check=True)
        nuget = result.stdout.decode('utf-8').strip()

        # Check that command is valid
        if os.path.exists(nuget) :
            break

    if verbose :
        print("NuGet executable found at {}".format(nuget))

    #====================
    #== Append sources ==
    #====================

    nuget_cli = NuGetCli(mono, nuget, verbose)

    print("-- Adding repository {} ({})".format(args.name, args.url))

    try :
        nuget_cli.sources  ("add", args.name, args.url, args.user, args.api_key, args.password_in_clear)
    except subprocess.CalledProcessError as e :
        nuget_cli.sources  ("update", args.name, args.url, args.user, args.api_key, args.password_in_clear)

    nuget_cli.setapikey(args.name, args.user, args.api_key)

    print("-- Success")

    return 0

#
# Description
#   The script main wrapper
#
if __name__ == "__main__":
    try :
      sys.exit(main(sys.argv[1:]))
    except Exception as e :
      print(e)
      sys.exit(1)
