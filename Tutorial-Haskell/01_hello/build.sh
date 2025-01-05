#!/usr/bin/env bash

BUILD_DIR=build
if [ ! -d "$BUILD_DIR" ]; then
    echo "Creating build dir: ${BUILD_DIR}/"
    mkdir $BUILD_DIR
fi
file="$1"
executable="${file%.hs}"

# -o     : Executable name
# -odir  : Output directory for object files (.o)
# -hidir : Output directory for haskell interface files (.hi)
echo "Compiling $file to $BUILD_DIR/"
ghc \
    -o ${BUILD_DIR}/${executable} \
    -odir ${BUILD_DIR} \
    -hidir ${BUILD_DIR} \
    $file

