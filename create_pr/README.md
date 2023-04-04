# create_pr

## example

```
# command
$ export GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>
$ export GITHUB_USER=<COMMIT_USERNAME>
$ export GITHUB_EMAIL=<COMMIT_USEREMAIL>
$ git diff | python create_pr.py -o <REPOSITORY_USER> -r <REPOSITORY_NAME> -c '<PR_COMMENT>' --head-branch <HEAD_BRANCH_NAME>

# docker
$ git diff | docker run --rm -e GITHUB_TOKEN=<YOUR_GITHUB_TOKEN> -e GITHUB_USER=<COMMIT_USERNAME> -e GITHUB_EMAIL=<COMMIT_USEREMAIL> -i create_pr -o <REPOSITORY_USER> -r <REPOSITORY_NAME> -c '<PR_COMMENT>' --head-branch <HEAD_BRANCH_NAME>
```