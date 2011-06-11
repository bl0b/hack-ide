#!/bin/sh
test "$0" = "./build.sh" || (echo "This script must be invoked from its directory ! like ./build.sh" && exit 1)
echo Running CMake and CPack...
cmake -DCMAKE_INSTALL_PREFIX=/usr .. && cpack
echo Cleaning up...
rm -rf CMakeCache.txt CMakeFiles cmake_install.cmake CPackConfig.cmake _CPack_Packages CPackSourceConfig.cmake install_manifest.txt Makefile usr/
echo Packages available:
ls hackide*
