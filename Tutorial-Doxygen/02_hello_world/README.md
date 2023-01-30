Take note of the edits to the Doxyfile by diffing it with the default
```bash
diff Doxyfile ../default_Doxyfile
```

Read through the cpp file to see how doxygen comments look.

To produce the doxygen documentation, run
```bash
doxygen Doxyfile
open docs/html/index.html
```

To compile the cpp executable, run
```bash
g++ -o hello_world hello_world.cpp
```
