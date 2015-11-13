#!/usr/bin/env python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# Usage:
#    gclient-new-workdir.py <repository> <new_workdir> [<branch>]
#

import os
import shutil
import subprocess
import sys
import textwrap

import git_common


def print_err(msg):
  print >> sys.stderr, msg


def usage(msg=None):

  if msg is not None:
    print_err('\n' + textwrap.dedent(msg) + '\n')
    usage_msg = 'Run without arguments to get usage help.'
  else:
    usage_msg = '''\
    usage: %s <repository> <new_workdir>

    Clone an existing gclient directory, taking care of all sub-repositories
    Works similarly to 'git new-workdir'.

    <repository> should contain a .gclient file
    <new_workdir> must not exist
    '''% os.path.basename(sys.argv[0])

  print_err(textwrap.dedent(usage_msg))
  sys.exit(1)


def parse_options():
  if sys.platform == 'win32':
    usage('This script cannot run on Windows because it uses symlinks.')

  if len(sys.argv) != 3:
    usage()

  repository = os.path.abspath(sys.argv[1])
  new_workdir = sys.argv[2]

  if not os.path.exists(repository):
    usage('Repository does not exist: ' + repository)

  if os.path.exists(new_workdir):
    usage('New workdir already exists: ' + new_workdir)

  return repository, new_workdir


def main():
  repository, new_workdir = parse_options()

  gclient = os.path.join(repository, '.gclient')
  if not os.path.exists(gclient):
    print_err('No .gclient file: ' + gclient)

  os.makedirs(new_workdir)
  os.symlink(gclient, os.path.join(new_workdir, '.gclient'))

  for root, dirs, _ in os.walk(repository):
    if '.git' in dirs:
      workdir = root.replace(repository, new_workdir, 1)
      print('Creating: %s' % workdir)
      git_common.make_workdir(os.path.join(root, '.git'),
                              os.path.join(workdir, '.git'))
      subprocess.check_call(['git', 'checkout', '-f'],
                            cwd=new_workdir.rstrip('.git'))


if __name__ == '__main__':
  sys.exit(main())
