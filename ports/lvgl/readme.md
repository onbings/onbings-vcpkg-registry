# Usage
 
**Only the json for now !**
 
## Vcpkg configuration
 
Add ``lvgl`` to
 
- `vcpkg.json`
- `vcpkg-configuration.json`
 
## CMake Integration
 
Add the following lines to your CMakeLists.txt
 
```cmake
# Find the package
find_package(lvgl REQUIRED)
 
# Link with the library
target_link_library(YOUR_TARGET PRIVATE EVS (???) ::lvgl)
```