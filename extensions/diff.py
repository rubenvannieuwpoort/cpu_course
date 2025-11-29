# import pykatex

from mistune.core import BaseRenderer, BlockState
from mistune.block_parser import BlockParser

import subprocess
from typing import Match

COMMIT_PATTERN = r"^!!(?P<commitmsg>.*)$"

commit_map = {}

def commit_diff(repo: str):
    global commit_map

    gitlog = subprocess.check_output(["git", "log", "--pretty=oneline", "--reverse"],text=True,cwd=repo)
    commit_map = { msg: sha for sha, msg in (line.split(" ", 1) for line in gitlog.splitlines()) }

    def f(repo, md):
        md.block.register('commit', COMMIT_PATTERN, parse_commit, before='list')
        if md.renderer and md.renderer.NAME == 'html':
            md.renderer.register('commit', lambda a, b: render_commit(a, b, repo))

    return lambda md: f(repo, md)


def parse_commit(_: BlockParser, m: Match[str], state: BlockState) -> int:
    commitmsg = m.group('commitmsg').strip()
    commitsha = commit_map[commitmsg]
    state.append_token({"type": "commit", "raw": commitsha})
    return m.end() + 1


def render_commit(_: BaseRenderer, text: str, repo: str) -> str:
    return get_diff2html_output(repo, text)


def get_diff2html_output(repo: str, commit_sha: str) -> str:
    if is_remote(repo):
        diff_command = ['curl', f'{repo}/commit/{commit_sha}.diff']
        cwd = None
    else:
        diff_command = ['git', 'diff', f'{commit_sha}^..{commit_sha}', '--no-prefix']
        cwd = repo

    diff2html_command = ['npx', 'diff2html-cli@5.2.15', '-i', 'stdin', '--hwt', 'templates/diff2html', '-o', 'stdout', '--style', 'side', '--fileContentToggle', 'true', '--summary', 'hidden', '--synchronisedScroll', 'true']

    diff = subprocess.run(diff_command, cwd=cwd, capture_output=True, text=True, check=True)
    diff2html = subprocess.run(diff2html_command, input=diff.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return diff2html.stdout


def is_remote(repo: str):
    return repo.startswith('https://')
