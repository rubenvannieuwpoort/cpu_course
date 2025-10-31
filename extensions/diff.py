# import pykatex

from mistune.core import BaseRenderer, BlockState
from mistune.block_parser import BlockParser

import subprocess
from typing import Match

COMMIT_PATTERN = r"^!!(?P<commitsha>.*)$"


def commit_diff(repo: str):
    def f(repo, md):
        md.block.register('commit', COMMIT_PATTERN, parse_commit, before='list')
        if md.renderer and md.renderer.NAME == 'html':
            md.renderer.register('commit', lambda a, b: render_commit(a, b, repo))

    return lambda md: f(repo, md)


def parse_commit(_: BlockParser, m: Match[str], state: BlockState) -> int:
    text = m.group('commitsha')
    state.append_token({"type": "commit", "raw": text})
    return m.end() + 1


def render_commit(_: BaseRenderer, text: str, repo: str) -> str:
    return get_diff2html_output(repo, text)


def get_diff2html_output(repo: str, commit_sha: str) -> str:
    if is_remote(repo):
        diff_command = ['curl', f'{repo}/commit/{commit_sha}.diff']
    else:
        diff_command = []
    diff2html_command = ['npx', 'diff2html-cli@5.2.15', '-i', 'stdin', '--hwt', 'templates/diff2html', '-o', 'stdout', '--style', 'side', '--fileContentToggle', 'false', '--summary', 'hidden', '--synchronisedScroll', 'true']

    try:
        # Run curl command and capture its output
        curl_process = subprocess.Popen(diff_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        assert curl_process.stdout is not None
        diff2html_process = subprocess.Popen(diff2html_command, stdin=curl_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        curl_process.stdout.close()
        stdout, stderr = diff2html_process.communicate()

        # Check for errors
        if diff2html_process.returncode != 0:
            raise subprocess.CalledProcessError(
                diff2html_process.returncode, diff2html_command, stderr=stderr
            )

        # Check for curl errors
        curl_stderr = curl_process.communicate()[1]
        if curl_process.returncode != 0:
            raise subprocess.CalledProcessError(
                curl_process.returncode, diff_command, stderr=curl_stderr
            )

        return stdout

    except subprocess.CalledProcessError as e:
        raise Exception(f"Command failed with error: {e.stderr}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


def is_remote(repo: str):
    return repo.startswith('https://')
