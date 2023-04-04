#!/usr/bin/env python
import argparse
import json
import os
import shutil
import subprocess
from urllib.request import Request, urlopen

GITHUB_USER = os.getenv('GITHUB_USER')
GITHUB_EMAIL = os.getenv('GITHUB_EMAIL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_HOST = os.getenv('GITHUB_HOST', 'github.com')

# for GHE
# export GITHUB_API_HOST=xxxxxx.com/api/v3
GITHUB_API_HOST = os.getenv('GITHUB_API_HOST', 'api.github.com')


def _parse_arguments():
    """
    parse arguments.

    :return:
    """
    parser = argparse.ArgumentParser(description='Create pull request.')
    parser.add_argument('-o', '--organization', metavar='ORGANIZATION', required=True,
                        help='repository user or organization')
    parser.add_argument('-r', '--repository', metavar='REPOSITORY', required=True, help='repository name')
    parser.add_argument('-c', '--commit-message', metavar='COMMIT_MESSAGE', required=True,
                        help='commit message when creating a branch and commiting a diff')
    parser.add_argument('-b', '--base-branch', metavar='BASE_BRANCH', default='main', required=False,
                        help='base branch name')
    parser.add_argument('--head-branch', metavar='HEAD_BRANCH', required=True, help='head branch name')
    parser.add_argument("--input-diff-file", type=argparse.FileType("r"), default="-")
    return parser.parse_args()


def _clone_repository(organization, repository):
    """
    clone repository.

    :param organization:
    :param repository:
    :return:
    """
    clone_url = f'https://{GITHUB_USER}:{GITHUB_TOKEN}@{GITHUB_HOST}/{organization}/{repository}'
    subprocess.run(['git', 'clone', clone_url])


def _create_local_branch(head_branch):
    """
    create local branch,

    :param head_branch:
    :return:
    """
    subprocess.run(['git', 'checkout', '-b', head_branch])


def _apply_patch(patch):
    """
    apply patch,

    :param patch:
    :return:
    """
    with open('diff.patch', 'w') as patch_file:
        patch_file.write(patch)
    subprocess.run(['git', 'apply', 'diff.patch'])
    os.remove('diff.patch')


def _commit_and_push_changes(head_branch, commit_message):
    """
    commit and push changes.

    :param head_branch:
    :param commit_message:
    :return:
    """
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', '-c', f'user.name="{GITHUB_USER}"', '-c', f'user.email="{GITHUB_EMAIL}"', 'commit',  '-m', commit_message])
    subprocess.run(['git', 'push', 'origin', head_branch])


def _create_pull_request(organization, repository, base_branch, head_branch) -> str:
    """
    create pull request.

    :param organization:
    :param repository:
    :param base_branch:
    :param head_branch:
    :return:
    """
    post_data_dict = {
        'title': 'PR title',
        'body': 'PR body',
        'head': head_branch,
        'base': base_branch
    }
    post_data = json.dumps(post_data_dict)
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-type': 'application/json'
    }
    create_pull_request_url = f'https://{GITHUB_API_HOST}/repos/{organization}/{repository}/pulls'
    request = Request(create_pull_request_url, post_data.encode('utf-8'), headers)
    with urlopen(request) as response:
        response_json = response.read().decode('utf-8')
        pull_request_response = json.loads(response_json)
        return pull_request_response['html_url']


if __name__ == '__main__':
    # parse args
    args = _parse_arguments()
    # remove already exists directory
    if os.path.exists(args.repository):
        shutil.rmtree(args.repository)
    # clone target repository
    _clone_repository(args.organization, args.repository)
    # change directory to clone repository directory.
    os.chdir(f'./{args.repository}')
    # create local branch
    _create_local_branch(args.head_branch)
    # apply patch
    patch_text = args.input_diff_file.read()
    _apply_patch(patch_text)
    # commit and push diff
    _commit_and_push_changes(args.head_branch, args.commit_message)
    # create pull request
    pull_request_url = _create_pull_request(args.organization, args.repository, args.base_branch, args.head_branch)
    print(f'=== Pull Request URL: {pull_request_url} ===')

