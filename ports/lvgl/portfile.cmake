# Retrieve the sources from github at a specific revision
# put 0 as initial SHA512 to get the "good" value
#   Expected hash : [ 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ]
#     Actual hash : [ 67cb71f5f324aa7249d33b58d3dbeef62abe68bcd59c1404959e672217e3ef806a8cd0e71d2b69d91a7927f7ff984c930a23697d592643f749745c645d0bc71e ]

vcpkg_from_github(
  OUT_SOURCE_PATH SOURCE_PATH
  REPO onbings/lvgl
  REF d543497f7b062b158f3c6446745d5df139339b49
  SHA512 d274b2fefcf2fbad3e0be4e19d4db28b9f627dc3e269fbcfede8a5a8c8d4d83dce6c87fe831feb0bb0f50b12f65dec2a3514640c9c37b7d8361399d9f53020da
  HEAD_REF main
)

# CMake configure : disable optional artifacts
vcpkg_configure_cmake(
  SOURCE_PATH "${SOURCE_PATH}"
  PREFER_NINJA
        OPTIONS
          -Dbof2d_BUILD_TESTS=OFF
          -Dbof2d_BUILD_TOOLS=OFF
          -Dbof2d_BUILD_EXAMPLES=OFF  
		  -Dbof2d_GENERATE_HELP=OFF		  
)

# CMake install
vcpkg_install_cmake()

# Fix installation path according to vcpkg conventions
vcpkg_fixup_cmake_targets(CONFIG_PATH share TARGET_PATH "share/bof2d")
vcpkg_copy_pdbs()

# Remove useless directories
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

# Make sure there is a copyright file
file(WRITE ${CURRENT_PACKAGES_DIR}/share/lvgl/copyright "")
#file(INSTALL "${SOURCE_PATH}/LICENSE" DESTINATION "${CURRENT_PACKAGES_DIR}/share/bof2d" RENAME copyright)
