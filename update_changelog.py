import os
import sys
import datetime
from github import Github
from dateutil.parser import parse

commit_sha = sys.argv[1]
github_token = sys.argv[2]

g = Github(github_token)

repo = g.get_repo("veeralakrishna/DataCamp-Project-Solutions-Python")

def get_associated_issues_prs(commit_sha):
    commit = repo.get_commit(commit_sha)
    commit_date = parse(commit.commit.author.date)

    issues = repo.get_issues(state="closed", since=commit_date)
    prs = repo.get_pulls(state="closed", sort="created", direction="desc", base=commit_sha)

    associated_issues_prs = []

    for issue in issues:
        associated_issues_prs.append(f"Issue {issue.number}: {issue.title}")

    for pr in prs:
        associated_issues_prs.append(f"PR {pr.number}: {pr.title}")

    return associated_issues_prs

def update_changelog(commit_sha):
    associated_issues_prs = get_associated_issues_prs(commit_sha)

    with open("changelog.md", "a") as changelog_file:
        changelog_file.write("\n\n")
        changelog_file.write(f"## {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
        changelog_file.write("### Changes\n")
        changelog_file.write(f"- [Commit {commit_sha[:7]}](https://github.com/veeralakrishna/DataCamp-Project-Solutions-Python/commit/{commit_sha})\n")
        changelog_file.write("### Associated Issues/PRs\n")
        changelog_file.write('\n'.join([f"- {item}" for item in associated_issues_prs]))

if __name__ == "__main__":
    update_changelog(commit_sha)
