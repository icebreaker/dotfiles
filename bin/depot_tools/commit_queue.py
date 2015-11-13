#!/usr/bin/env python
# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Access the commit queue from the command line.
"""

__version__ = '0.1'

import functools
import json
import logging
import optparse
import os
import sys
import urllib2

import breakpad  # pylint: disable=W0611

import auth
import fix_encoding
import rietveld

THIRD_PARTY_DIR = os.path.join(os.path.dirname(__file__), 'third_party')
sys.path.insert(0, THIRD_PARTY_DIR)

from cq_client import cq_pb2
from cq_client import validate_config
from protobuf26 import text_format

def usage(more):
  def hook(fn):
    fn.func_usage_more = more
    return fn
  return hook


def need_issue(fn):
  """Post-parse args to create a Rietveld object."""
  @functools.wraps(fn)
  def hook(parser, args, *extra_args, **kwargs):
    old_parse_args = parser.parse_args

    def new_parse_args(args=None, values=None):
      options, args = old_parse_args(args, values)
      auth_config = auth.extract_auth_config_from_options(options)
      if not options.issue:
        parser.error('Require --issue')
      obj = rietveld.Rietveld(options.server, auth_config, options.user)
      return options, args, obj

    parser.parse_args = new_parse_args

    parser.add_option(
        '-u', '--user',
        metavar='U',
        default=os.environ.get('EMAIL_ADDRESS', None),
        help='Email address, default: %default')
    parser.add_option(
        '-i', '--issue',
        metavar='I',
        type='int',
        help='Rietveld issue number')
    parser.add_option(
        '-s',
        '--server',
        metavar='S',
        default='http://codereview.chromium.org',
        help='Rietveld server, default: %default')
    auth.add_auth_options(parser)

    # Call the original function with the modified parser.
    return fn(parser, args, *extra_args, **kwargs)

  hook.func_usage_more = '[options]'
  return hook


def set_commit(obj, issue, flag):
  """Sets the commit bit flag on an issue."""
  try:
    patchset = obj.get_issue_properties(issue, False)['patchsets'][-1]
    print obj.set_flag(issue, patchset, 'commit', flag)
  except urllib2.HTTPError, e:
    if e.code == 404:
      print >> sys.stderr, 'Issue %d doesn\'t exist.' % issue
    elif e.code == 403:
      print >> sys.stderr, 'Access denied to issue %d.' % issue
    else:
      raise
    return 1

@need_issue
def CMDset(parser, args):
  """Sets the commit bit."""
  options, args, obj = parser.parse_args(args)
  if args:
    parser.error('Unrecognized args: %s' % ' '.join(args))
  return set_commit(obj, options.issue, '1')


@need_issue
def CMDclear(parser, args):
  """Clears the commit bit."""
  options, args, obj = parser.parse_args(args)
  if args:
    parser.error('Unrecognized args: %s' % ' '.join(args))
  return set_commit(obj, options.issue, '0')


def CMDbuilders(parser, args):
  """Prints json-formatted list of builders given a path to cq.cfg file.

  The output is a dictionary in the following format:
    {
      'master_name': [
        'builder_name',
        'another_builder'
      ],
      'another_master': [
        'third_builder'
      ]
    }
  """
  _, args = parser.parse_args(args)
  if len(args) != 1:
    parser.error('Expected a single path to CQ config. Got: %s' %
                 ' '.join(args))

  with open(args[0]) as config_file:
    cq_config = config_file.read()

  config = cq_pb2.Config()
  text_format.Merge(cq_config, config)
  masters = {}
  if config.HasField('verifiers') and config.verifiers.HasField('try_job'):
    for bucket in config.verifiers.try_job.buckets:
      masters.setdefault(bucket.name, [])
      for builder in bucket.builders:
        if not builder.HasField('experiment_percentage'):
          masters[bucket.name].append(builder.name)
  print json.dumps(masters)

CMDbuilders.func_usage_more = '<path-to-cq-config>'


def CMDvalidate(parser, args):
  """Validates a CQ config.

  Takes a single argument - path to the CQ config to be validated. Returns 0 on
  valid config, non-zero on invalid config. Errors and warnings are printed to
  screen.
  """
  _, args = parser.parse_args(args)
  if len(args) != 1:
    parser.error('Expected a single path to CQ config. Got: %s' %
                 ' '.join(args))

  with open(args[0]) as config_file:
    cq_config = config_file.read()
  return 0 if validate_config.IsValid(cq_config) else 1

CMDvalidate.func_usage_more = '<path-to-cq-config>'

###############################################################################
## Boilerplate code


class OptionParser(optparse.OptionParser):
  """An OptionParser instance with default options.

  It should be then processed with gen_usage() before being used.
  """
  def __init__(self, *args, **kwargs):
    optparse.OptionParser.__init__(self, *args, **kwargs)
    self.add_option(
        '-v', '--verbose', action='count', default=0,
        help='Use multiple times to increase logging level')

  def parse_args(self, args=None, values=None):
    options, args = optparse.OptionParser.parse_args(self, args, values)
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging.basicConfig(
        level=levels[min(len(levels) - 1, options.verbose)],
        format='%(levelname)s %(filename)s(%(lineno)d): %(message)s')
    return options, args

  def format_description(self, _):
    """Removes description formatting."""
    return self.description.rstrip() + '\n'


def Command(name):
  return getattr(sys.modules[__name__], 'CMD' + name, None)


@usage('<command>')
def CMDhelp(parser, args):
  """Print list of commands or use 'help <command>'."""
  # Strip out the help command description and replace it with the module
  # docstring.
  parser.description = sys.modules[__name__].__doc__
  parser.description += '\nCommands are:\n' + '\n'.join(
      '  %-12s %s' % (
        fn[3:], Command(fn[3:]).__doc__.split('\n', 1)[0].rstrip('.'))
      for fn in dir(sys.modules[__name__]) if fn.startswith('CMD'))

  _, args = parser.parse_args(args)
  if len(args) == 1 and args[0] != 'help':
    return main(args + ['--help'])
  parser.print_help()
  return 0


def gen_usage(parser, command):
  """Modifies an OptionParser object with the command's documentation.

  The documentation is taken from the function's docstring.
  """
  obj = Command(command)
  more = getattr(obj, 'func_usage_more')
  # OptParser.description prefer nicely non-formatted strings.
  parser.description = obj.__doc__ + '\n'
  parser.set_usage('usage: %%prog %s %s' % (command, more))


def main(args=None):
  # Do it late so all commands are listed.
  # pylint: disable=E1101
  parser = OptionParser(version=__version__)
  if args is None:
    args = sys.argv[1:]
  if args:
    command = Command(args[0])
    if command:
      # "fix" the usage and the description now that we know the subcommand.
      gen_usage(parser, args[0])
      return command(parser, args[1:])

  # Not a known command. Default to help.
  gen_usage(parser, 'help')
  return CMDhelp(parser, args)


if __name__ == "__main__":
  fix_encoding.fix_encoding()
  try:
    sys.exit(main())
  except KeyboardInterrupt:
    sys.stderr.write('interrupted\n')
    sys.exit(1)
