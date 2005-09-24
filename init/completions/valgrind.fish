
if valgrind --version | grep -- '-2\.[012]\.' >/dev/null ^/dev/null
	# In older versions of Valgrind, the skin selection option was
    # '--skin'
	set -g skin skin
else
	# But someone decided that it would be fun to change this to
    # '--tool' for no good reason
	set -g skin tool
end

complete -xc valgrind -l $skin -d "Skin" -a "
	memcheck\tHeavyweight\ memory\ checker
	cachegrind\tCache-miss\ profiler
	addrcheck\tLightweight\ memory\ checker
	helgrind\tData-race\ detector
	massif\tHeap\ profiler
"
set -e $skin

complete -c valgrind -l help -d "Display help and exit"
complete -c valgrind -l help-debug -d "Display help and debug options"
complete -c valgrind -l version -d "Print version"
complete -c valgrind -s q -l quiet -d "Run silently"
complete -c valgrind -s v -l verbose -d "Verbose mode"
complete -xc valgrind -l trace-children -d "Valgrind-ise children" -a "yes no"
complete -xc valgrind -l track-fds -d "Track file descriptors" -a "yes no"
complete -xc valgrind -l logfile-fd -d "Log to file descriptor" -a "0 1 2 3 4 5 6 7 8 9"
complete -rc valgrind -l logfile -d "Log to file"
complete -xc valgrind -l logsocket -d "Log to socket"
complete -c valgrind -l demangle -xd "Demangle C++ names" -a "yes no"
complete -xc valgrind -l num-callers -d "Callers in stack trace"
complete -xc valgrind -l error-limit -d "Stop showing errors if too many" -a "yes no"
complete -xc valgrind -l show-below-main -d "Continue trace below main()" -a "yes no"
complete -rc valgrind -l supressions -d "Supress errors from file"
complete -c valgrind -l gen-supressions -d "Print suppressions for detected errors"
complete -xc valgrind -l db-attach -d "Start debugger on error" -a "yes no"
complete -rc valgrind -l db-command -d "Debugger command"
complete -xc valgrind -l input-fd -d "File descriptor for input" -a "0 1 2 3 4 5 6 7 8 9"


# Memcheck-specific options
complete -n "contains -- --skin=memcheck (commandline -cpo)" -xc valgrind -l leak-check -d "Check for memory leaks" -a "no\t'Do not check for memory leaks' summary\t'Show a leak summary' full\t'Describe memory leaks in detail'"
complete -n "contains -- --skin=memcheck (commandline -cpo)" -xc valgrind -l show-reachable -d "Show reachable leaked memory" -a "yes\t'Show reachable leaked memory' no\t'Do not show reachable leaked memory'"
complete -n "contains -- --skin=memcheck (commandline -cpo)" -xc valgrind -l leak-resolution -d "Determines how willing Memcheck is to consider different backtraces to be the same" -a "low\t'Two entries need to match' med\t'Four entries need to match' high\t'All entries need to match'"
complete -n "contains -- --skin=memcheck (commandline -cpo)" -xc valgrind -l freelist-vol -d "Set size of freed memory pool"
complete -n "contains -- --skin=memcheck (commandline -cpo)" -xc valgrind -l partial-loads-ok -d 'How to handle loads of words that are partially addressible' -a 'yes\t"Do not emit errors on partial loads" no\t"Emit errors on partial loads"'
complete -n "contains -- --skin=memcheck (commandline -cpo)" -xc valgrind -l avoid-strlen-errors -d 'Whether to skip error reporting for the strlen function' -a 'yes no'


# Addrcheck-specific options
complete -n "contains -- --skin=addrcheck (commandline -cpo)" -xc valgrind -l leak-check -d "Check for memory leaks" -a "no\t'Do not check for memory leaks' summary\t'Show a leak summary' full\t'Describe memory leaks in detail'"
complete -n "contains -- --skin=addrcheck (commandline -cpo)" -xc valgrind -l show-reachable -d "Show reachable leaked memory" -a "yes\t'Show reachable leaked memory' no\t'Do not show reachable leaked memory'"
complete -n "contains -- --skin=addrcheck (commandline -cpo)" -xc valgrind -l leak-resolution -d "Determines how willing Addrcheck is to consider different backtraces to be the same" -a "low\t'Two entries need to match' med\t'Four entries need to match' high\t'All entries need to match'"
complete -n "contains -- --skin=addrcheck (commandline -cpo)" -xc valgrind -l freelist-vol -d "Set size of freed memory pool"
complete -n "contains -- --skin=addrcheck (commandline -cpo)" -xc valgrind -l partial-loads-ok -d 'How to handle loads of words that are partially addressible' -a 'yes\t"Do not emit errors on partial loads" no\t"Emit errors on partial loads"'
complete -n "contains -- --skin=addrcheck (commandline -cpo)" -xc valgrind -l avoid-strlen-errors -d 'Whether to skip error reporting for the strlen function' -a 'yes no'

# Cachegrind-specific options
complete -n "contains -- --skin=cachegrind (commandline -cpo)" -xc valgrind -l I1 -d "Type of L1 instruction cache"
complete -n "contains -- --skin=cachegrind (commandline -cpo)" -xc valgrind -l D1 -d "Type of L1 data cache"
complete -n "contains -- --skin=cachegrind (commandline -cpo)" -xc valgrind -l L2 -d "Type of L2 cache"


# Massif-specific options
complete -c valgrind -n "contains -- --skin=massif (commandline -cpo)" -l alloc-fn -d "Specify a function that allocates memory"
complete -c valgrind -n "contains -- --skin=massif (commandline -cpo)" -x -l heap -d 'Profile heap usage' -a 'yes\t"Profile heap usage" no\t"Do not profile heap usage"'
complete -c valgrind -n "contains -- --skin=massif (commandline -cpo)" -x -l heap-admin -d "The number of bytes of heap overhead per allocation"
complete -c valgrind -n "contains -- --skin=massif (commandline -cpo)" -x -l stacks -d "Profile stack usage" -a 'yes\t"Profile stack usage" no\t"Do not profile stack usage"'
complete -c valgrind -n "contains -- --skin=massif (commandline -cpo)" -x -l depth -d "Depth of call chain"
complete -c valgrind -n "contains -- --skin=massif (commandline -cpo)" -x -l format -d "Profiling output format" -a "html\t'Produce html output' text\t'Produce text output'"
