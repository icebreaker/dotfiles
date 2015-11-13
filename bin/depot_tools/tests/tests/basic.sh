#!/usr/bin/env bash

# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

set -e

. ./test-lib.sh

setup_initsvn
setup_gitsvn

(
  set -e
  cd git-svn
  git checkout -q -b work
  echo "some work done on a branch" >> test
  git add test; git commit -q -m "branch work"
  echo "some other work done on a branch" >> test
  git add test; git commit -q -m "branch work"

  test_expect_success "git-cl upload wants a server" \
    "$GIT_CL upload --no-oauth2 2>&1 | grep -q 'You must configure'"

  git config rietveld.server localhost:10000

  test_expect_success "git-cl status has no issue" \
    "$GIT_CL_STATUS | grep -q 'No issue assigned'"

  # Prevent the editor from coming up when you upload.
  export GIT_EDITOR=$(which true)

  test_expect_success "upload succeeds (needs a server running on localhost)" \
    "$GIT_CL upload --no-oauth2 -m test master | grep -q 'Issue created'"

  test_expect_success "git-cl status now knows the issue" \
    "$GIT_CL_STATUS | grep -q 'Issue number'"

  # Push a description to this URL.
  URL=$($GIT_CL_STATUS | sed -ne '/Issue number/s/[^(]*(\(.*\))/\1/p')
  curl --cookie dev_appserver_login="test@example.com:False" \
       --data-urlencode subject="test" \
       --data-urlencode description="foo-quux" \
       --data-urlencode xsrf_token="$(print_xsrf_token)" \
       $URL/edit

  test_expect_success "git-cl dcommits ok" \
    "$GIT_CL dcommit -f --no-oauth2"

  git checkout -q master
  git svn -q rebase >/dev/null 2>&1
  test_expect_success "dcommitted code has proper description" \
      "git show | grep -q 'foo-quux'"

  test_expect_success "issue no longer has a branch" \
      "$GIT_CL_STATUS | grep -q 'work : None'"

  test_expect_success "upstream svn has our commit" \
      "svn log $REPO_URL 2>/dev/null | grep -q 'foo-quux'"
)
SUCCESS=$?

cleanup

if [ $SUCCESS == 0 ]; then
  echo PASS
fi
