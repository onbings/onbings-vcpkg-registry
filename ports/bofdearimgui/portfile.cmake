# Retrieve the sources from github at a specific revision
# put 0 as initial SHA512 to get the "good" value
#   Expected hash : [ 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ]
#     Actual hash : [ 67cb71f5f324aa7249d33b58d3dbeef62abe68bcd59c1404959e672217e3ef806a8cd0e71d2b69d91a7927f7ff984c930a23697d592643f749745c645d0bc71e ]

#https://github.com/microsoft/vcpkg/pull/16613
#set(VCPKG_USE_HEAD_VERSION ON)

vcpkg_from_github(
  OUT_SOURCE_PATH SOURCE_PATH
  REPO onbings/bofdearimgui
  REF 1ffd0f1ca7039766db4c90c3e34e8feb18295c4b
  SHA512 4074b0cc1c955c36014e50795b95cb542eaaa7916617c53236416c2f41ff77e7d96a660719d671c5844e4b836c14044ce77afcc40540413d0bc46ed208afe4cf
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
