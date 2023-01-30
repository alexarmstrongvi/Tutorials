#!/usr/bin/env bash
################################################################################
# Examples of testing variables are set, empty, or non-empty
################################################################################
unset unset_var
set_null_var=
set_empty_var=""
set_nonempty_var="abcd"

# Tests
# -z : tests if no characters are there after expansion
# -n : tests if any characters are there after expansion
# -v : 

# NOTE: print_error function defined in LexEnv repo

################################################################################
# Check if variable is not set
# Assert true
[ -z ${unset_var+x} ] || print_error "FAILED 1"
# Assert false
[ -z ${set_null_var+x} ] && print_error "FAILED 2"
[ -z ${set_empty_var+x} ] && print_error "FAILED 3"
[ -z ${set_nonempty_var+x} ] && print_error "FAILED 4"

################################################################################
# Check if variable is set
# Same as above but replace "-z" with "-n"
# Assert true
[ -n "${set_null_var+x}" ] || print_error "FAILED 6"
[ -n "${set_empty_var+x}" ] || print_error "FAILED 6"
[ -n "${set_nonempty_var+x}" ] || print_error "FAILED 7"
# Assert false
[ -n "${unset_var+x}" ] && print_error "FAILED 8"

################################################################################
# Check if variable is set to null or empty string (same thing for bash)
# see https://unix.stackexchange.com/questions/280430/are-the-null-string-and-the-same-string
# Assert true
[ -z ${set_empty_var-x} ] || print_error "FAILED 9"
[ -z ${set_null_var-x} ] || print_error "FAILED 10"
# Assert false
[ -z ${unset_var-x} ] && print_error "FAILED 11"
[ -z ${set_nonempty_var-x} ] && print_error "FAILED 12"

################################################################################
# Check if variable is set to non-empty string
# Assert true
[ -n "$set_nonempty_var" ] || print_error "FAILED 13"
# Assert false
[ -n "$unset_var" ] && print_error "FAILED 14"
[ -n "$set_null_var" ] && print_error "FAILED 15"
[ -n "$set_empty_var" ] && print_error "FAILED 16"

################################################################################
# Checks that don't do what you think they are doing

# Wrong way to check if var is nonempty
[ -n $unset_var ] || print_error "FAILED"
[ -n $set_null_var ] || print_error "FAILED"
[ -n $set_empty_var ] || print_error "FAILED"
# All tests above return true because they expand to "[ -n  ]" which returns true



