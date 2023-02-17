#!/usr/bin/env bash
if [ -f HelloWorld ]; then
    rm HelloWorld
fi
if [ -f HelloWorld.o ]; then
    rm HelloWorld.o
fi
make
./HelloWorld
# rm HelloWorld HelloWorld.o

