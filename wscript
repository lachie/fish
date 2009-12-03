# /usr/bin/env python
import re
import Options
import sys, os, shutil
from Utils import cmd_output, subst_vars
from os.path import join, dirname, abspath
from logging import fatal

cwd = os.getcwd()
VERSION="1.23.1"
APPNAME="fish"

srcdir = '.'
blddir = 'build'

sources_for_tasks = {
  'fish': """
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
  """,
  'fishd': """
    src/fishd.c
    src/env_universal_common.c
    src/wutil.c
    src/print_help.c
    src/common.c
  """,
  'fish_pager': """
    src/fish_pager.c
    src/output.c
    src/wutil.c
    src/input_common.c
    src/env_universal.c
    src/env_universal_common.c
    src/common.c
    src/print_help.c
  """,
  'fish_indent': """
    src/fish_indent.c
    src/print_help.c
    src/common.c
    src/parser_keywords.c
    src/wutil.c
    src/tokenizer.c
  """,
  'mimedb': """
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
}

def set_options(opt):
  opt.tool_options('compiler_cc')
  opt.tool_options('misc')
  opt.add_option( '--debug'
                , action='store_true'
                , default=False
                , help='Build debug variant [Default: False]'
                , dest='debug'
                )

def configure(conf):
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
  conf.env.append_value('CCFLAGS',  '-D_FILE_OFFSET_BITS=64')

  # platform
  platform_def = '-DPLATFORM=' + sys.platform
  conf.env.append_value('CCFLAGS', platform_def)

  # Split off debug variant before adding variant specific defines
  debug_env = conf.env.copy()
  conf.set_env_name('debug', debug_env)

  # Configure debug variant
  conf.setenv('debug')
  debug_env.set_variant('debug')
  debug_env.append_value('CCFLAGS', ['-DDEBUG', '-g', '-O0', '-Wall', '-Wextra'])
  conf.write_config_header("config.h")

  # Configure default variant
  conf.setenv('default')
  conf.env.append_value('CCFLAGS', ['-DNDEBUG', '-O3'])
  conf.write_config_header("config.h")

def build_task(bld, name, extra_linkflags = None):
  task = bld.new_task_gen("cc", "program")
  task.name = name
  task.target = name
  task.source = sources_for_tasks[name]
  task.ccflags = [
    "-std=c99",
    "-g",
    "-O2",
    "-Wall",
    "-rdynamic",
    "-iquote../include"
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
  
  task.linkflags = [
    "-lncurses"
  ]
  if extra_linkflags != None:
    task.linkflags.append(extra_linkflags)
  
  bld.install_files('${PREFIX}/bin/', [name])
  
  task.chmod = 0755
  return task

def build(bld):
  build_task(bld, "fish", "-liconv")
  build_task(bld, "fishd", "-liconv")
  build_task(bld, "fish_pager", "-liconv")
  build_task(bld, "fish_indent")
  build_task(bld, "mimedb")

  bld.install_files('${PREFIX}/share/man/man1/', 'share/man/*')
