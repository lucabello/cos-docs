---
title: Operations
summary: Guidelines on team-specific operations.
author: Luca Bello
date: 2023-01-25
---
# Operations

## GitHub CI

Our charm repositories make use of a shared CI defined in the [canonical/observability](https://github.com/canonical/observability) repo. Let's have a look at how that is invoked and configured to analyze what the CI is doing and how to add it to a new charm.  
I'll use the files in the [Prometheus' charm workflows](https://github.com/canonical/prometheus-k8s-operator/tree/main/.github/workflows) as an example:

* [codeql-analysis.yml](https://github.com/canonical/prometheus-k8s-operator/blob/main/.github/workflows/codeql-analysis.yml) runs a CodeQL analysis (GitHub engine mostly for security checks)
* [issues.yaml](https://github.com/canonical/prometheus-k8s-operator/blob/main/.github/workflows/issues.yaml) automatically handles the creation of Jira tickets from GitHub issues
* [promote.yaml](https://github.com/canonical/prometheus-k8s-operator/blob/main/.github/workflows/promote.yaml) is manual action to promote a charm to its *next* channel (i.e., from *edge* to *candidate*, from *candidate* to *stable*)
* [pull-request.yaml](https://github.com/canonical/prometheus-k8s-operator/blob/main/.github/workflows/pull-request.yaml) starts a series of quality checks on PRs (i.e., linting, static checks, testing, and more)
* [release-edge.yaml](https://github.com/canonical/prometheus-k8s-operator/blob/main/.github/workflows/release-edge.yaml) handles the automatic release of a charm to edge whenever a PR is merged to *main* (if it's passing the quality checks)
* [release-libs.yaml](https://github.com/canonical/prometheus-k8s-operator/blob/main/.github/workflows/release-libs.yaml) automatically publishes the charm libraries that have been updated and version-bumped on PR merges to *main*
* [update-libs.yaml](https://github.com/canonical/prometheus-k8s-operator/blob/main/.github/workflows/update-libs.yaml) periodically checks if some charm libraries are outdated, and if so opens a PR with the necessary updates to be manually reviewed and merged

Note that introducing this CI for a new charm requires the addition of some secrets in your repository:

* `CHARMHUB_TOKEN` for the `charmcraft` command operations
* `OBSERVABILITY_NOCTUA_TOKEN` for the automatic PR creation on library updates

## Manually publish a Charm

Charm releases and promotions usually happen through the CI; however, sometimes it might be necessary to do it manually:
```bash
charmcraft pack
# Login to charmcraft
charmcraft login --export=~/charmcraft.auth
export CHARMCRAFT_AUTH=$(cat ~/charmcraft.auth)
# Upload the charm and get the revision number
charmcraft upload <packed_charm> # The <revision> number will be printed
```

Check in the charm metadata to see what resources are needed by the charm, and then:
```bash
# Find out the latest revision of the resources to attach
charmcraft resource-revisions <charm_name> <resource>
# Release the charm to some channel
charmcraft release <charm_name> \
	--revision=<charm_revision> \
	--channel=<channel> \
	--resource=<resource_name>:<resource_revision>
## example:
## charmcraft release traefik-k8s \
##     --revision=94 \
##     --channel=edge \
##     --resource=traefik-image:88
```
