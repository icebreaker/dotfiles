# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import sys

import recipe_util  # pylint: disable=F0401


# This class doesn't need an __init__ method, so we disable the warning
# pylint: disable=W0232
class SkiaBuildbot(recipe_util.Recipe):
  """Basic Recipe class for the Skia Buildbot repository."""

  @staticmethod
  def fetch_spec(_props):
    solution = {
      'name'     : 'buildbot',
      'url'      : 'https://skia.googlesource.com/buildbot.git',
      'deps_file': 'DEPS',
      'managed'  : False,
    }
    spec = {
      'solutions': [solution]
    }
    return {
        'type': 'gclient_git',
        'gclient_git_spec': spec,
    }

  @staticmethod
  def expected_root(_props):
    return 'buildbot'


def main(argv=None):
  return SkiaBuildbot().handle_args(argv)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
