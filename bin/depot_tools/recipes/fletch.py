# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import sys

import recipe_util  # pylint: disable=F0401

# This class doesn't need an __init__ method, so we disable the warning
# pylint: disable=W0232
class Fletch(recipe_util.Recipe):
  """Basic Recipe class for Fletch."""

  @staticmethod
  def fetch_spec(props):
    url = 'https://github.com/dart-lang/fletch.git'
    solution = {
      'name'   :'fletch',
      'url'    : url,
      'deps_file': 'DEPS',
      'managed'   : False,
      'custom_deps': {},
      'safesync_url': '',
    }
    spec = {
      'solutions': [solution],
    }
    if props.get('target_os'):
      spec['target_os'] = props['target_os'].split(',')
    return {
      'type': 'gclient_git',
      'gclient_git_spec': spec,
    }

  @staticmethod
  def expected_root(_props):
    return 'fletch'


def main(argv=None):
  return Fletch().handle_args(argv)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
