message( STATUS "INFO :: Calling CMake (version ${CMAKE_VERSION}) located at ${CMAKE_COMMAND}" )
message( STATUS "INFO :: Generating build files for project located at ${CMAKE_CURRENT_SOURCE_DIR}" )
message( STATUS "INFO :: Build files will be stored at :: ${CMAKE_CURRENT_BINARY_DIR}" )

cmake_minimum_required(VERSION 3.11)

# Require out-of-source builds
file(TO_CMAKE_PATH "${CMAKE_CURRENT_BINARY_DIR}/CMakeLists.txt" LOC_PATH)
if(EXISTS "${LOC_PATH}")
    message(FATAL_ERROR "Do not build in a source directory (or any directory with a CMakeLists.txt file). Please make a build/ subdirectory.")
endif()

project(02_simple_cmake
    VERSION # major.minor.patch.tweak
        1.0.0.0
    LANGUAGES
        CXX # Default
)

add_executable(hello_world hello_world.cxx)

message( STATUS "INFO :: New project created -> ${PROJECT_NAME} (version ${PROJECT_VERSION})" )

message( STATUS "VERBOSE :: Other variables" )
# CURRENT is important when the project is included as a subdirectory in another project
# Variables without CURRENT reference the top most project instead of the project currently being built by CMake
message( STATUS "VERBOSE :: CMAKE_BINARY_DIR           = ${CMAKE_BINARY_DIR}" )
message( STATUS "VERBOSE :: CMAKE_CURRENT_BINARY_DIR   = ${CMAKE_CURRENT_BINARY_DIR}" )
message( STATUS "VERBOSE :: 02_simple_cmake_BINARY_DIR = ${02_simple_cmake_BINARY_DIR}" )
message( STATUS "VERBOSE :: PROJECT_BINARY_DIR         = ${PROJECT_BINARY_DIR}" )
message( STATUS "VERBOSE :: CMAKE_SOURCE_DIR           = ${CMAKE_SOURCE_DIR}" )
message( STATUS "VERBOSE :: CMAKE_CURRENT_SOURCE_DIR   = ${CMAKE_CURRENT_SOURCE_DIR}" )
message( STATUS "VERBOSE :: 02_simple_cmake_SOURCE_DIR = ${02_simple_cmake_SOURCE_DIR}" )
message( STATUS "VERBOSE :: PROJECT_SOURCE_DIR         = ${PROJECT_SOURCE_DIR}" )
message( STATUS "VERBOSE :: CMAKE_PROJECT_NAME = ${CMAKE_PROJECT_NAME}" )
message( STATUS "VERBOSE :: PROJECT_NAME       = ${PROJECT_NAME}" )
message( STATUS "VERBOSE :: CMAKE_INCLUDE_PATH = ${CMAKE_INCLUDE_PATH}" )
message( STATUS "VERBOSE :: CMAKE_LIBRARY_PATH = ${CMAKE_LIBRARY_PATH}" )
message( STATUS "VERBOSE :: CMAKE_PREFIX_PATH  = ${CMAKE_PREFIX_PATH}" )
message( STATUS "VERBOSE :: CMAKE_CXX_COMPILER = ${CMAKE_CXX_COMPILER}" )
message( STATUS "VERBOSE :: CMAKE_CXX_FLAGS = ${CMAKE_CXX_FLAGS}" )


