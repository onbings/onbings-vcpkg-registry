# Retrieve the sources from github at a specific revision
# put 0 as initial SHA512 to get the "good" value
#   Expected hash : [ 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 ]
#     Actual hash : [ 67cb71f5f324aa7249d33b58d3dbeef62abe68bcd59c1404959e672217e3ef806a8cd0e71d2b69d91a7927f7ff984c930a23697d592643f749745c645d0bc71e ]

vcpkg_from_github(
  OUT_SOURCE_PATH SOURCE_PATH
  REPO onbings/bofstd
  REF 567d327c00275479eb9fc9a520ba7c740cc7268
  SHA512 91f2ca250950b8eaf6f931fdc6de1e61bf59eb0f76b19e79feb96a2e8301bcc26c8a84c48692a577b9f867240233a44bf1042b44c9dc2def15abe4f5c3b0dcb2
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
