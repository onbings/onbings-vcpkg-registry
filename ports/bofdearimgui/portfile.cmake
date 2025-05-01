# Retrieve the sources from github at a specific revision
# put 0 as initial SHA512 to get the "good" value
#   Expected hash : [ 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ]
#     Actual hash : [ 67cb71f5f324aa7249d33b58d3dbeef62abe68bcd59c1404959e672217e3ef806a8cd0e71d2b69d91a7927f7ff984c930a23697d592643f749745c645d0bc71e ]

#https://github.com/microsoft/vcpkg/pull/16613
#set(VCPKG_USE_HEAD_VERSION ON)

vcpkg_from_github(
  OUT_SOURCE_PATH SOURCE_PATH
  REPO onbings/bofdearimgui
  REF 066fa6fe4410b62fa6d18dd2723fdae347c17142
  SHA512 57c84ba287fa7cb313ed44a7f6d1f8cae06d9c188bac6ac10fd27149803e0f30130e2123955cfc7d3c5b01e1d831a24ae468d776b9d4a399179c848a388f277c
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
#set(VCPKG_POLICY_SKIP_MISPLACED_CMAKE_FILES_CHECK enabled)  #due to special gtest
vcpkg_install_cmake()

# Fix installation path according to vcpkg conventions
vcpkg_fixup_cmake_targets(CONFIG_PATH share TARGET_PATH "share/bofdearimgui")
vcpkg_copy_pdbs()

# Remove useless directories
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

# Make sure there is a copyright file
file(WRITE ${CURRENT_PACKAGES_DIR}/share/bofdearimgui/copyright "")
#file(INSTALL "${SOURCE_PATH}/LICENSE" DESTINATION "${CURRENT_PACKAGES_DIR}/share/bofdearimgui" RENAME copyright)
