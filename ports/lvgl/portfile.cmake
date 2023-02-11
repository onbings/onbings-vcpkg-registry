# Retrieve the sources from github at a specific revision
# put 0 as initial SHA512 to get the "good" value
#   Expected hash : [ 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ]
#     Actual hash : [ 67cb71f5f324aa7249d33b58d3dbeef62abe68bcd59c1404959e672217e3ef806a8cd0e71d2b69d91a7927f7ff984c930a23697d592643f749745c645d0bc71e ]

vcpkg_from_github(
  OUT_SOURCE_PATH SOURCE_PATH
  REPO onbings/lvgl
  REF 114878766e53e7e456b84a94506ad4ac04f173c9
  SHA512 fc1e46606c9d4654c66c03849c6e27da9354961808f027449a7f73c67a81c46a2950f994ee83dce2d2b94232df83324df78f45e7799ed2957e360332a5063df6
  HEAD_REF main
)

# CMake configure : disable optional artifacts
vcpkg_configure_cmake(
  SOURCE_PATH "${SOURCE_PATH}"
  PREFER_NINJA
        OPTIONS
          -Dlvgl_BUILD_TESTS=OFF
          -Dlvgl_BUILD_TOOLS=OFF
          -Dlvgl_BUILD_EXAMPLES=OFF  
		  -Dlvgl_GENERATE_HELP=OFF		  
)

# CMake install
vcpkg_install_cmake()

# Fix installation path according to vcpkg conventions
vcpkg_fixup_cmake_targets(CONFIG_PATH share TARGET_PATH "share/bof2d")
vcpkg_copy_pdbs()
message("===========CURRENT_PACKAGES_DIR==================>" ${CURRENT_PACKAGES_DIR})

# Remove useless directories
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

# Make sure there is a copyright file
file(WRITE ${CURRENT_PACKAGES_DIR}/share/lvgl/copyright "")
#file(INSTALL "${SOURCE_PATH}/LICENSE" DESTINATION "${CURRENT_PACKAGES_DIR}/share/bof2d" RENAME copyright)
