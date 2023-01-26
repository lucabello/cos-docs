#!/usr/bin/env python3

def define_env(env):
    "Hook function"

    GIT_URL="https://github.com"

    @env.macro
    def ghbadge(stage, repository):
        """Return the Markdown for a CI badge of the specified action and repository."""
        repository_url = _build_repository_url(repository)
        stage_url = f"{repository_url}/actions/workflows/{stage}.yaml"
        svg_url = f"{stage_url}/badge.svg"
        return f"[![{stage}]({svg_url})]({stage_url})"

    @env.macro
    def repoentry(repository, show_github=True, show_charmhub=True):
        """Return a table entry for a repository in a pretty format.

        Specifically, given the repository name this function will produce the following format:
        <repository_name> [github-icon](link to repo) [canonical-icon](link to charmhub)
        """
        repository_url = _build_repository_url(repository)
        charmhub_url = _build_charmhub_url(repository)
        github_icon = f"[:simple-github:]({repository_url})" if show_github else ""
        charmhub_icon = f"[:simple-canonical:]({charmhub_url})" if show_charmhub else ""
        return f"{repository} &nbsp;&nbsp; {github_icon} {charmhub_icon}"
    
    def _build_repository_url(repository_name, org="canonical"):
        """Build the repository URL starting from its name."""
        return f"{GIT_URL}/{org}/{repository_name}"

    def _build_charmhub_url(repository_name):
        """Build the Charmhub URL starting from a repository name."""
        charmhub_name = repository_name.rsplit("-operator", 1)[0]
        charmhub_name = charmhub_name.rsplit("-bundle", 1)[0]
        return f"https://charmhub.io/{charmhub_name}"
