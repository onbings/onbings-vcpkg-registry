# Usage
 
**Only the json for now !**
 
## Vcpkg configuration
 
Add ``bof2d`` to
 
- `vcpkg.json`
- `vcpkg-configuration.json`
 
## CMake Integration
 
Add the following lines to your CMakeLists.txt
 
```cmake
# Find the package
find_package(bof2d REQUIRED)
 
# Link with the library
target_link_library(YOUR_TARGET PRIVATE EVS (???) ::bof2d)
```