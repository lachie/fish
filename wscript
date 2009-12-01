# /usr/bin/env python
import re
import Options
import sys, os, shutil
from Utils import cmd_output, subst_vars
from os.path import join, dirname, abspath
from logging import fatal

cwd = os.getcwd()
VERSION="0.1.20"
APPNAME="node.js"

srcdir = '.'
blddir = 'build'

def set_options(opt):
  # the gcc module provides a --debug-level option
  opt.tool_options('compiler_cxx')
  opt.tool_options('compiler_cc')
  opt.tool_options('misc')
  opt.add_option( '--debug'
                , action='store_true'
                , default=False
                , help='Build debug variant [Default: False]'
                , dest='debug'
                )
  opt.add_option( '--efence'
                , action='store_true'
                , default=False
                , help='Build with -lefence for debugging [Default: False]'
                , dest='efence'
                )

def mkdir_p(dir):
  if not os.path.exists (dir):
    os.makedirs (dir)

# Copied from Python 2.6 because 2.4.4 at least is broken by not using
# mkdirs
# http://mail.python.org/pipermail/python-bugs-list/2005-January/027118.html
def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = join(src, name)
        dstname = join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error), why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error, err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Error, errors

def configure(conf):
  conf.check_tool('compiler_cxx')
  conf.check_tool('compiler_cc')

  conf.env["USE_DEBUG"] = Options.options.debug

  conf.check(lib='dl', uselib_store='DL')
  conf.env.append_value("CCFLAGS", "-rdynamic")
  conf.env.append_value("LINKFLAGS_DL", "-rdynamic")

  #if Options.options.debug:
  #  conf.check(lib='profiler', uselib_store='PROFILER')

  #if Options.options.efence:
  #  conf.check(lib='efence', libpath=['/usr/lib', '/usr/local/lib'], uselib_store='EFENCE')

  # conf.sub_config('deps/libeio')
  # conf.sub_config('deps/libev')

  # conf_subproject(conf, 'deps/udns', './configure')

  conf.define("HAVE_CONFIG_H", 1)

  conf.env.append_value("CCFLAGS", "-DX_STACKSIZE=%d" % (1024*64))

  # LFS
  conf.env.append_value('CCFLAGS',  '-D_LARGEFILE_SOURCE')
  conf.env.append_value('CXXFLAGS', '-D_LARGEFILE_SOURCE')
  conf.env.append_value('CCFLAGS',  '-D_FILE_OFFSET_BITS=64')
  conf.env.append_value('CXXFLAGS', '-D_FILE_OFFSET_BITS=64')

  # platform
  platform_def = '-DPLATFORM=' + sys.platform
  conf.env.append_value('CCFLAGS', platform_def)
  conf.env.append_value('CXXFLAGS', platform_def)

  # Split off debug variant before adding variant specific defines
  debug_env = conf.env.copy()
  conf.set_env_name('debug', debug_env)

  # Configure debug variant
  conf.setenv('debug')
  debug_env.set_variant('debug')
  debug_env.append_value('CCFLAGS', ['-DDEBUG', '-g', '-O0', '-Wall', '-Wextra'])
  debug_env.append_value('CXXFLAGS', ['-DDEBUG', '-g', '-O0', '-Wall', '-Wextra'])
  conf.write_config_header("config.h")

  # Configure default variant
  conf.setenv('default')
  conf.env.append_value('CCFLAGS', ['-DNDEBUG', '-O3'])
  conf.env.append_value('CXXFLAGS', ['-DNDEBUG', '-O3'])
  conf.write_config_header("config.h")

def make_task(bld, name):
  task = bld.new_task_gen("cc", "program")
  task.name = name
  task.target = name
  task.ccflags = [
    "-std=c99",
    "-g",
    "-O2",
    "-Wall",
    "-rdynamic",
    "-iquote../include"
  ]
  task.linkflags = [
    "-lncurses"
  ]
  task.defines = map(lambda s: subst_vars(s, bld.env), [
    'PREFIX=L"${PREFIX}"',
    'DATADIR=L"${PREFIX}/share"',
    'SYSCONFDIR=L"${PREFIX}/etc"',
    'LOCALEDIR="${PREFIX}/share/locale"'
  ])
  task.includes = """
    src/
  """
  task.uselib_local = ''
  task.install_path = '${PREFIX}/lib'
  task.install_path = '${PREFIX}/bin'
  task.chmod = 0755
  return task

def build(bld):
  fish = make_task(bld, "fish")
  fish.linkflags.append("-liconv")
  fish.source = """
    src/function.c
    src/builtin.c
    src/complete.c
    src/env.c
    src/exec.c
    src/expand.c
    src/highlight.c
    src/history.c
    src/kill.c
    src/parser.c
    src/proc.c
    src/reader.c
    src/sanity.c
    src/tokenizer.c
    src/wildcard.c
    src/wgetopt.c
    src/wutil.c
    src/input.c
    src/output.c
    src/intern.c
    src/env_universal.c
    src/env_universal_common.c
    src/input_common.c
    src/event.c
    src/signal.c
    src/io.c
    src/parse_util.c
    src/common.c
    src/screen.c
    src/path.c
    src/parser_keywords.c
    src/fish.c
  """
  
  mimedb = make_task(bld, "mimedb")
  mimedb.source = """
    src/mimedb.c
    src/print_help.c
    src/xdgmimealias.c
    src/xdgmime.c
    src/xdgmimeglob.c
    src/xdgmimeint.c
    src/xdgmimemagic.c
    src/xdgmimeparent.c
    src/wutil.c
    src/common.c
  """

  fish_pager = make_task(bld, "fish_pager")
  fish_pager.linkflags.append("-liconv")
  fish_pager.source = """
    src/fish_pager.c
    src/output.c
    src/wutil.c
    src/input_common.c
    src/env_universal.c
    src/env_universal_common.c
    src/common.c
    src/print_help.c
  """
  
  fishd = make_task(bld, "fishd")
  fishd.linkflags.append("-liconv")
  fishd.source = """
    src/fishd.c
    src/env_universal_common.c
    src/wutil.c
    src/print_help.c
    src/common.c
  """
  
  fish_indent = make_task(bld, "fish_indent")
  fish_indent.source = """
    src/fish_indent.c
    src/print_help.c
    src/common.c
    src/parser_keywords.c
    src/wutil.c
    src/tokenizer.c
  """

  bld.install_files('${PREFIX}/include/node/', """
    config.h
    src/node.h
    src/node_object_wrap.h
    src/node_events.h
    src/node_net.h
  """)

  # Only install the man page if it exists. 
  # Do 'make doc install' to build and install it.
  if os.path.exists('doc/node.1'):
    bld.install_files('${PREFIX}/share/man/man1/', 'doc/node.1')

  bld.install_files('${PREFIX}/bin/', 'bin/*', chmod=0755)

  # Why am I using two lines? Because WAF SUCKS.
  bld.install_files('${PREFIX}/lib/node/wafadmin', 'tools/wafadmin/*.py')
  bld.install_files('${PREFIX}/lib/node/wafadmin/Tools', 'tools/wafadmin/Tools/*.py')

  bld.install_files('${PREFIX}/lib/node/libraries/', 'lib/*.js')

def shutdown():
  Options.options.debug
  # HACK to get binding.node out of build directory.
  # better way to do this?
  if not Options.commands['clean']:
    if os.path.exists('build/default/node') and not os.path.exists('node'):
      os.symlink('build/default/node', 'node')
    if os.path.exists('build/debug/node_g') and not os.path.exists('node_g'):
      os.symlink('build/debug/node_g', 'node_g')
  else:
    if os.path.exists('node'): os.unlink('node')
    if os.path.exists('node_g'): os.unlink('node_g')
