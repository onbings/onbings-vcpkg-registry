# Retrieve the sources from github at a specific revision
# put 0 as initial SHA512 to get the "good" value
#   Expected hash : [ 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ]
#     Actual hash : [ 67cb71f5f324aa7249d33b58d3dbeef62abe68bcd59c1404959e672217e3ef806a8cd0e71d2b69d91a7927f7ff984c930a23697d592643f749745c645d0bc71e ]

#https://github.com/microsoft/vcpkg/pull/16613
#set(VCPKG_USE_HEAD_VERSION ON)

vcpkg_from_github(
  OUT_SOURCE_PATH SOURCE_PATH
  REPO onbings/bofwebrpc
  REF 6209d62caa29b1aaae4f0ec12906f55a74227dfa
  SHA512 62faa1ab80f6e2a23c14fd901ce45be45b2aa227f84c36eeff547981c27bc7d53357b8d126d16b2453208eeb7dda12c4877cdc539e6c25663eec491e6ed792ad
  HEAD_REF main
)

# CMake configure : disable optional artifacts
vcpkg_configure_cmake(
  SOURCE_PATH "${SOURCE_PATH}"
  PREFER_NINJA
        OPTIONS
#		-DRHEL="el9" 
)

# CMake install
vcpkg_install_cmake()

# Fix installation path according to vcpkg conventions
vcpkg_fixup_cmake_targets(CONFIG_PATH share TARGET_PATH "share/bofwebrpc")
vcpkg_copy_pdbs()

# Remove useless directories
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

# Make sure there is a copyright file
file(WRITE ${CURRENT_PACKAGES_DIR}/share/bofwebrpc/copyright "")
#file(INSTALL "${SOURCE_PATH}/LICENSE" DESTINATION "${CURRENT_PACKAGES_DIR}/share/bofwebrpc" RENAME copyright)
