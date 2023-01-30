if [ -n "${OLD_PROMPT+x}" ]; then
    echo "Resetting to original prompt"
    PROMPT="$OLD_PROMPT"
    unset OLD_PROMPT
    return 0
fi
echo "Rerun script to reset prompt"
OLD_PROMPT="$PROMPT"
# Default prompt
PROMPT='%n@%m %1~ %#'

# Prompt parameters
PROMPT='PROMPT Demo:
Login Information
%%l = %l
%%M = %M
%%m = %m
%%n = %n
%%y = %y
Shell State Information
%%? = %?
%%d = %d
%%~ = %~
%%h = %h
%%C = %C
Date and Time Information
%%D = %D
%%T = %T
%%t = %t
%%* = %*
%%w = %w
%%W = %W
Visual Elements
%BBold%b
%UUnderline%u
%SHighlight%s
%F{red}Font Color%f
%K{green}Background Color%k
>> '
# Recognized colors: black, red, green, yellow, blue, magenta, cyan and white