#
# Main file for fish command completions. This file contains various
# common helper functions for the command completions. All actual
# completions are located in the completions subdirectory.
#

#
# Set default field separators
#

set -g IFS \n\ \t

# The install prefix the one containing bin/fish.
set -l install_prefix (echo (which fish) | sed 's/\/bin\/fish$//')

#
# Set default search paths for completions and shellscript functions
# unless they already exist
#

set -l configdir ~/.config

if set -q XDG_CONFIG_HOME
	set configdir $XDG_CONFIG_HOME
end

# These are used internally by fish in various places
if not set -q __fish_datadir
	set -g __fish_datadir $install_prefix/share/fish
end

if not set -q __fish_sysconfdir
	set -g __fish_sysconfdir $install_prefix/etc/fish
end

# Set up function and completion paths. Make sure that the fish
# default functions/completions are included in the respective path.

if not set -q fish_function_path 
	set -U fish_function_path $configdir/fish/functions    $install_prefix/etc/fish/functions    $install_prefix/share/fish/functions 
end

if not contains $install_prefix/share/fish/functions $fish_function_path
	set fish_function_path[-1] $install_prefix/share/fish/functions
end

if not set -q fish_complete_path 
	set -U fish_complete_path $configdir/fish/completions  $install_prefix/etc/fish/completions  $install_prefix/share/fish/completions 
end

if not contains $install_prefix/share/fish/completions $fish_complete_path
	set fish_complete_path[-1] $install_prefix/share/fish/completions
end

set __fish_help_dir $install_prefix/share/doc/

#
# This is a Solaris-specific test to modify the PATH so that
# Posix-conformant tools are used by default. It is separate from the
# other PATH code because this directory needs to be prepended, not
# appended, since it contains POSIX-compliant replacements for various
# system utilities.
#

if test -d /usr/xpg4/bin
	if not contains /usr/xpg4/bin $PATH
		set PATH /usr/xpg4/bin $PATH 
	end
end   

#
# Add a few common directories to path, if they exists. Note that pure
# console programs like makedep sometimes live in /usr/X11R6/bin, so we
# want this even for text-only terminals.
#

set -l path_list /usr/local/bin /usr/bin /bin /usr/X11/bin $install_prefix/bin

# Root should also have the sbin directories in the path
switch $USER
	case root
	set path_list $path_list /usr/local/sbin /usr/sbin /sbin $install_prefix/bin
end

for i in $path_list
	if not contains $i $PATH
		if test -d $i
			set PATH $PATH $i
		end
	end
end

#
# Launch debugger on SIGTRAP
#
function fish_sigtrap_handler --on-signal TRAP --no-scope-shadowing --description "Signal handler for the TRAP signal. Lanches a debug prompt."
	breakpoint
end

#
# Whenever a prompt is displayed, make sure that interactive
# mode-specific initializations have been performed.
# This handler removes itself after it is first called.
#
function __fish_on_interactive --on-event fish_prompt
	__fish_config_interactive
	functions -e __fish_on_interactive
end

