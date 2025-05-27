# Retrieve the sources from github at a specific revision
# put 0 as initial SHA512 to get the "good" value
#   Expected hash : [ 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ]
#     Actual hash : [ 67cb71f5f324aa7249d33b58d3dbeef62abe68bcd59c1404959e672217e3ef806a8cd0e71d2b69d91a7927f7ff984c930a23697d592643f749745c645d0bc71e ]

#https://github.com/microsoft/vcpkg/pull/16613
#set(VCPKG_USE_HEAD_VERSION ON)

vcpkg_from_github(
  OUT_SOURCE_PATH SOURCE_PATH
  REPO onbings/bofstd
  REF fbf1fe2447a85aa1b89838f7bacbd6048762c51c
  SHA512 cca71c47c3685601b3820cdd6d64c560072e60f2ef5a27cb9adc8b1d23baf7b98c33b142a9d1d53e5c9f3ccffa1a825995ae1b05798004f7fde3909cc8053aa5
  HEAD_REF main
)

# CMake configure : disable optional artifacts
vcpkg_configure_cmake(
  SOURCE_PATH "${SOURCE_PATH}"
  PREFER_NINJA
        OPTIONS
          -DBOFSTD_BUILD_TESTS=OFF
          -DBOFSTD_BUILD_TOOLS=OFF
          -DBOFSTD_BUILD_EXAMPLES=OFF  
		  -DBOFSTD_GENERATE_HELP=OFF		  
)

# CMake install
vcpkg_install_cmake()

# Fix installation path according to vcpkg conventions
vcpkg_fixup_cmake_targets(CONFIG_PATH share TARGET_PATH "share/bofstd")
vcpkg_copy_pdbs()

# Remove useless directories
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

# Make sure there is a copyright file
file(WRITE ${CURRENT_PACKAGES_DIR}/share/bofstd/copyright "")
#file(INSTALL "${SOURCE_PATH}/LICENSE" DESTINATION "${CURRENT_PACKAGES_DIR}/share/bofstd" RENAME copyright)
