file="$1"
./build.sh $file

if [ $? -eq 0 ]; then
    executable="./build/${file%.hs}"
    echo "Running ${executable}"
    echo
    ${executable}
else
    echo "Build failed"
fi
