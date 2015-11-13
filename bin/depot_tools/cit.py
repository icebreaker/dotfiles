#!/usr/bin/env python
# Copyright (c) 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


"""Wrapper for updating and calling infra.git tools.

This tool does a two things:
* Maintains a infra.git checkout pinned at "deployed" in the home dir
* Acts as an alias to infra.tools.*
"""

# TODO(hinoka): Use cipd/glyco instead of git/gclient.

import argparse
import sys
import os
import subprocess
import re


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GCLIENT = os.path.join(SCRIPT_DIR, 'gclient.py')
TARGET_DIR = os.path.expanduser('~/.chrome-infra')
INFRA_DIR = os.path.join(TARGET_DIR, 'infra')


def get_git_rev(target, branch):
  return subprocess.check_output(
      ['git', 'log', '--format=%B', '-n1', branch], cwd=target)


def need_to_update(branch):
  """Checks to see if we need to update the ~/.chrome-infra/infra checkout."""
  try:
    cmd = [sys.executable, GCLIENT, 'revinfo']
    subprocess.check_call(
        cmd, cwd=os.path.join(TARGET_DIR), stdout=subprocess.PIPE)
  except subprocess.CalledProcessError:
    return True  # Gclient failed, definitely need to update.
  except OSError:
    return True  # Gclient failed, definitely need to update.

  local_rev = get_git_rev(INFRA_DIR, 'HEAD')

  subprocess.check_call(
      ['git', 'fetch', 'origin'], cwd=INFRA_DIR,
      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  origin_rev = get_git_rev(INFRA_DIR, 'origin/%s' % (branch,))
  return origin_rev != local_rev


def ensure_infra(branch):
  """Ensures that infra.git is present in ~/.chrome-infra."""
  print 'Fetching infra@%s into %s, may take a couple of minutes...' % (
      branch, TARGET_DIR)
  if not os.path.isdir(TARGET_DIR):
    os.mkdir(TARGET_DIR)
  if not os.path.exists(os.path.join(TARGET_DIR, '.gclient')):
    subprocess.check_call(
        [sys.executable, os.path.join(SCRIPT_DIR, 'fetch.py'), 'infra'],
        cwd=TARGET_DIR,
        stdout=subprocess.PIPE)
  subprocess.check_call(
      [sys.executable, GCLIENT, 'sync', '--revision', 'origin/%s' % (branch,)],
      cwd=TARGET_DIR,
      stdout=subprocess.PIPE)


def get_available_tools():
  tools = []
  starting = os.path.join(TARGET_DIR, 'infra', 'infra', 'tools')
  for root, _, files in os.walk(starting):
    if '__main__.py' in files:
      tools.append(root[len(starting)+1:].replace(os.path.sep, '.'))
  return tools


def run(args):
  if args:
    tool_name = args[0]
    cmd = [
        sys.executable, os.path.join(TARGET_DIR, 'infra', 'run.py'),
        'infra.tools.%s' % tool_name]
    cmd.extend(args[1:])
    return subprocess.call(cmd)

  tools = get_available_tools()
  print """usage: cit.py <name of tool> [args for tool]

  Wrapper for maintaining and calling tools in "infra.git/run.py infra.tools.*"

  Available tools are:
  """
  for tool in tools:
    print '  * %s' % tool


def main():
  parser = argparse.ArgumentParser("Chrome Infrastructure CLI.")
  parser.add_argument('-b', '--infra-branch', default='deployed',
      help="The name of the 'infra' branch to use (default is %(default)s).")
  parser.add_argument('args', nargs=argparse.REMAINDER)

  args, extras = parser.parse_known_args()
  if args.args and args.args[0] == '--':
    args.args.pop(0)
  if extras:
    args.args = extras + args.args

  if need_to_update(args.infra_branch):
    ensure_infra(args.infra_branch)
  return run(args.args)

if __name__ == '__main__':
  sys.exit(main())
