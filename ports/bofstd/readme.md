# Usage
 
**Only the json for now !**
 
## Vcpkg configuration
 
Add ``bofstd`` to
 
- `vcpkg.json`
- `vcpkg-configuration.json`
 
## CMake Integration
 
Add the following lines to your CMakeLists.txt
 
```cmake
# Find the package
find_package(bofstd REQUIRED)
 
# Link with the library
target_link_library(YOUR_TARGET PRIVATE EVS (???) ::bofstd)
```