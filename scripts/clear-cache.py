#!/usr/bin/env python3

import argparse
from collections import OrderedDict
import errno
import os
import pathlib
import shutil
import stat
import sys

#
# Description
#   This function removes read-only attribute
#   on file that we want to delete anyway
#
# Parameters
#   func - The calling function
#   path - The path to the file
#   exc  - the exception
#
# Returns
#    0 - The operation was successful
#   !0 - The operation failed
#
def remove_read_only_handler(func, path, exc):
  excvalue = exc[1]
  if excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

#
# Description
#   This function removes the specified directory
#
# Parameters
#   _path - The path to the directory to remove
#
# Returns
#    0 - The operation was successful
#   !0 - The operation failed
#
def remove_directory(_path):

    print("-- Removing directory : {}".format(_path))

    # Does the directory exists
    if os.path.exists(_path) :
        shutil.rmtree(_path, ignore_errors=False, onerror=remove_read_only_handler)
        print("--                    : OK")
    else :
        print("--                    : Not existing")

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
def main(argv):

    parser = argparse.ArgumentParser(description="This script clean cache(s) used by vcpkg")

    # Mandatory arguments
    requiredArguments = parser.add_argument_group('Mandatory arguments')

    # Optional arguments
    parser.add_argument("--all",             dest="all",             help="Clean everything",                                   action="store_true")
    parser.add_argument("--binary-cache",    dest="binary_cache",    help="Clean the binary cache",                             action="store_true")
    parser.add_argument("--build-folder",    dest="build_folder",    help="Clean the build folder in your vcpkg repository",    action="store_true")
    parser.add_argument("--download-folder", dest="download_folder", help="Clean the download folder in your vcpkg repository", action="store_true")
    parser.add_argument("--package-folder",  dest="package_folder",  help="Clean the package folder in your vcpkg repository",  action="store_true")
    parser.add_argument("--vcpkg-root",      dest="vcpkg_root",      help="The path to your vpckg root directory")

    args = parser.parse_args(argv)

    # Get current directory
    current_dir = str(pathlib.Path(__file__).parent.absolute())

    # Check arguments
    if args.all or args.build_folder or args.download_folder :
        if args.vcpkg_root :
            vcpkg_root = args.vcpkg_root
        elif "VCPKG_ROOT" in os.environ :
            vcpkg_root = os.environ["VCPKG_ROOT"]
        else :
            raise ValueError("You requested to clean build_folder and/or download_folder which are relatives to vcpkg_root\n"
                             "You did not specify where to vcpkg root is located so they cannot be found\n"
                             "This can be done either through --vcpkg-root option or VCPKG_ROOT environment variable")

    # Enforce all if requested
    if args.all :
        args.binary_cache = True
        args.build_folder = True
        args.download_folder = True
        args.package_folder = True

    # buildtrees folder is used by vcpkg
    # to build ports. It contains for each port
    #   - sources
    #   - binaries
    #   - logs
    if args.build_folder :
        remove_directory(os.path.join(args.vcpkg_root, "buildtrees"))

    # downloads folder is used by vcpkg
    # to download artifacts from various places
    # It mainly contains zipped sources
    if args.download_folder :
        remove_directory(os.path.join(args.vcpkg_root, "downloads"))

    # package folder is used by vcpkg
    # to install build artifacts
    if args.download_folder :
        remove_directory(os.path.join(args.vcpkg_root, "packages"))

    # binary cache is where vcpkg store compiled ports
    # identified by there compiler hash version
    if args.binary_cache :

        # If binary caching is used in conjunction with
        # VCPKG_USE_NUGET_CACHE it can store nuget into
        # <home_dir>/.nuget/packages
        if "USERPROFILE" in os.environ :
            home_dir = os.environ["USERPROFILE"]
        else :
            home_dir = os.environ["HOME"]

        remove_directory(os.path.join(home_dir, ".nuget", "packages"))

        # Search in order
        binary_cache_paths = OrderedDict([
          ("VCPKG_DEFAULT_BINARY_CACHE", ""),
          ("LOCALAPPDATA"              , "vcpkg"),
          ("APPDATA"                   , "vcpkg"),
          ("XDG_CACHE_HOME"            , "vcpkg"),
          ("HOME"                      , os.path.join(".cache", "vcpkg"))
        ])

        for var,subdir in binary_cache_paths.items() :
            if var in os.environ :
                remove_directory(os.path.join(os.environ[var], subdir))
                break

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
