echo "User         : $(whoami)"
echo "Node         : $(uname -n)"
echo "OS           : $(uname -s) ($(uname -r))"
echo "OS version   : $(uname -v)"
echo "Architecture : $(uname -m) (Processor : $(uname -p))"
echo

echo "Current folder disk usage"
du -h -d 0 .* *.* */ | sort -hr | awk '{printf("\t%02d) ", NR); print}'
echo

echo "Path variables"
path_vars=$(env | grep -Eo "[A-Z]*PATH[A-Z]*") 
for p in $path_vars; do echo "  $p"; printenv $p | tr ':' '\n' | awk '{printf("\t%02d) ", NR); print}'; done
echo

echo "Other environment variables" 
env | grep -v "PATH" | sort | column -t -s "=" | awk '{printf("\t%02d) ", NR); print}'
echo

echo "Filesystem"
mount | awk '{print "\t" NR ") " $0}'
echo

