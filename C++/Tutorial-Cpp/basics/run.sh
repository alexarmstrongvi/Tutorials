################################################################################
# Clean up files/folders leftover from previous run
if [ -f a.out ];      then rm a.out;         fi
if [ -d a.out.dSYM ]; then rm -r a.out.dSYM; fi 

################################################################################
echo "Compiling..."
clang++ \
    -Wall -Wextra -Wpedantic \
    -Werror \
    -pedantic-errors \
    -std=c++17 \
    -stdlib=libc++ \
    -g \
    basics.cpp

if [ $? -eq 0 ]; then
    printf "====== RUNNING ======\n"
    ./a.out
    printf "\n====== DONE ======\n"
else
    printf "\n====== FAILED ======\n"
fi
