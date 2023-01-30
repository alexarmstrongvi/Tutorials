How to compile and run
(Option 1)
```bash
mkdir build
cd build
cmake ..
make
./hello_world

```
(Option 2)
```bash
cmake -S . -B build
cmake --build build
./build/hello_world
```


How to clear all the CMake auto-generated files
```bash
rm -r build/*
```
