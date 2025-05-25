message( STATUS "INFO :: Generating build files for project located at ${CMAKE_CURRENT_SOURCE_DIR}" )
message( STATUS "INFO :: Build files stored at :: ${CMAKE_CURRENT_BINARY_DIR}" )

cmake_minimum_required( VERSION 3.15 )

# Require out-of-source builds
file(TO_CMAKE_PATH "${CMAKE_CURRENT_BINARY_DIR}/CMakeLists.txt" LOC_PATH)
if(EXISTS "${LOC_PATH}")
    message(FATAL_ERROR "Do not build in a source directory (or any directory with a CMakeLists.txt file). Please make a build/ subdirectory.")
endif()

# Create the project
project( 03_simple_project_structure 
        VERSION # major.minor.patch.tweak
            1.0.0.0
        LANGUAGES
            CXX
)
message( STATUS "INFO :: Project defined : ${PROJECT_NAME} (version ${PROJECT_VERSION})" )

# Create a library target for this project
# - This could be moved to a CMakeLists.txt file in the src directory
file(GLOB HEADER_LIST CONFIGURE_DEPENDS include/03_simple_project_structure/*.hpp)
add_library( 03_simple_project_structureLib
    # List source files in src/
    src/adder.cxx
    # List header files in include/ (optional but helpful)
    include/03_simple_project_structure/adder.h
    # -OR- 
    #${HEADER_LIST}
)
# Add directories to the library so that files are useable
target_include_directories(03_simple_project_structureLib PUBLIC include )

# Create an executable target
# - This could be moved to a CMakeLists.txt file in the apps directory
add_executable( add_and_print apps/add_and_print.cxx )
# Link all needed libraries for the executable
target_link_libraries( add_and_print 03_simple_project_structureLib )

