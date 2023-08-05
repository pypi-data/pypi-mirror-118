#
#     setup_scmversion - Automatic setting of semantic version numbers based
#                        on scm tags and branches.
#
#     Copyright (C) 2019 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import re
from functools import lru_cache
from typing import Tuple

from ..parser import ScmParser, Tags
from ..util import execute_command

# Copied from poetry/core/version/version.py - a hack
POETRY_VERSION_PATTERN = re.compile(
    r"""
    ^
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            [-_.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_.]?
                (?P<post_l>post|rev|r)
                [-_.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_.]?
            (?P<dev_l>dev)
            [-_.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_.][a-z0-9]+)*))?       # local version
    $
""",
    re.IGNORECASE | re.VERBOSE,
)


def is_valid_version(input):
    match = POETRY_VERSION_PATTERN.match(input)
    return False if not match else True


class GitError(Exception):
    pass


def validate_semantic_version(builder):
    def wrap(branch: str, commits: str, tag: str):
        type, version = builder(branch, commits, tag)
        if not is_valid_version(version):
            raise ValueError(f"invalid semantic version {version}")
        return type, version
    return wrap


class GitParser(ScmParser):

    def __init__(self, executor=execute_command):
        self.executor = executor

    def _git_command(self, command: str) -> str:
        out, err = self.executor(command)
        def flatten(x): return ''.join(x.split('\n'))
        flatten_out, flatten_err = flatten(out), flatten(err)
        if len(flatten_err) > 0:
            raise GitError(command, err, out)
        return flatten_out

    @property
    @lru_cache()
    def branch(self):
        return self._git_command('git rev-parse --abbrev-ref HEAD')

    @property
    @lru_cache()
    def commits(self):
        return int(self._git_command(f'git rev-list --count {self.branch}'))

    @property
    @lru_cache()
    def tag(self):
        try:
            tag = self._git_command('git describe --tags')
            # check for tag out of the ordinary, i.e.
            # fatal: No names found, cannot describe anything.
            if tag.startswith('fatal:'):
                logging.info(f'no previous tags: "{tag}"')
                tag = None
        except Exception:
            logging.exception('cannot describe tag, will use None')
            tag = None
        return tag

    @staticmethod
    @validate_semantic_version
    def build_version(branch: str, commits: str, tag: str) -> Tuple[Tags, str]:
        if branch in ['master', 'HEAD']:
            if tag is None:
                return Tags.OTHER, f'0.0.0+master.{commits}'
            elif is_valid_version(tag):
                if tag.count('-') <= 1:
                    return Tags.RELEASE, tag
                # arbitrary tags from git like '0.0.1-1-g5c0bb91'
                else:
                    return Tags.OTHER, tag
            else:
                tag = 'nothing' if tag == '' else tag
                return Tags.OTHER, f'0.0.0+master.{tag}.{commits}'
        elif branch.startswith('release/'):
            version = branch.split('/')[-1] + f'-dev{commits}'
            if is_valid_version(version):
                return (Tags.RELEASE_BRANCH, version)
            else:
                return Tags.OTHER, f'0.0.0+release.invalid.{commits}'
        elif branch.startswith('feature/'):
            version = branch.split('/')[-1] + f'+feature{commits}'
            if is_valid_version(version):
                return (Tags.FEATURE_BRANCH, version)
            else:
                return Tags.OTHER, f'0.0.0+feature.invalid.{commits}'
        else:
            version = '.'.join(
                [x for x in ['0.0.0+other', branch, tag, commits] if x != '']
            )
            return (Tags.OTHER, version.replace('/', '_'))

    def version(self, pre_commit: bool = False) -> str:
        """builds a version number based on information on the scm"""
        commits = self.commits + 1 if pre_commit else self.commits
        version = GitParser.build_version(self.branch, commits, self.tag)[1]
        return version

    def version_type(self) -> Tags:
        """finds the version type based on information on the scm"""
        return GitParser.build_version(self.branch, self.commits, self.tag)[0]
