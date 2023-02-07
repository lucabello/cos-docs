---
title: Status
summary: A page with the status of Canonical's Observability repos.
author: Luca Bello
date: 2023-01-25
---
# Status

This page contains the current status of all the charms managed by the Observability team.

## Github CI

| Charm                                                    | Release Charm                                                          | Release Libraries                                               |
| -------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------- |
| {{ repoentry("alertmanager-k8s-operator") }}             | {{ ghbadge("release-edge", "alertmanager-k8s-operator") }}             | {{ ghbadge("release-libs", "alertmanager-k8s-operator") }}      |
| {{ repoentry("avalanche-k8s-operator") }}                | {{ ghbadge("release-edge", "avalanche-k8s-operator") }}                | (no libraries)                                                  |
| {{ repoentry("catalogue-k8s-operator") }}                | {{ ghbadge("release-edge", "catalogue-k8s-operator") }}                | {{ ghbadge("release-libs", "catalogue-k8s-operator") }}         |
| {{ repoentry("cos-configuration-k8s-operator") }}        | {{ ghbadge("release-edge", "cos-configuration-k8s-operator") }}        | (no libraries)                                                  |
| {{ repoentry("grafana-agent-k8s-operator") }}            | {{ ghbadge("release-edge", "grafana-agent-k8s-operator") }}            | {{ ghbadge("release-libs", "grafana-agent-k8s-operator") }}     |
| {{ repoentry("grafana-k8s-operator") }}                  | {{ ghbadge("release-edge", "grafana-k8s-operator") }}                  | {{ ghbadge("release-libs", "grafana-k8s-operator") }}           |
| {{ repoentry("karma-k8s-operator") }}                    | {{ ghbadge("release-edge", "karma-k8s-operator") }}                    | {{ ghbadge("release-libs", "karma-k8s-operator") }}             |
| {{ repoentry("loki-k8s-operator") }}                     | {{ ghbadge("release-edge", "loki-k8s-operator") }}                     | {{ ghbadge("release-libs", "loki-k8s-operator") }}              |
| {{ repoentry("mimir-k8s-operator") }}                    | {{ ghbadge("release-edge", "mimir-k8s-operator") }}                    | {{ ghbadge("release-libs", "mimir-k8s-operator") }}             |
| {{ repoentry("prometheus-k8s-operator") }}               | {{ ghbadge("release-edge", "prometheus-k8s-operator") }}               | {{ ghbadge("release-libs", "prometheus-k8s-operator") }}        |
| {{ repoentry("prometheus-pushgateway-k8s-operator") }}   | {{ ghbadge("release-edge", "prometheus-pushgateway-k8s-operator") }}   | (no libraries)                                                  |
| {{ repoentry("prometheus-scrape-config-k8s-operator") }} | {{ ghbadge("release-edge", "prometheus-scrape-config-k8s-operator") }} | (no libraries)                                                  |
| {{ repoentry("prometheus-scrape-target-k8s-operator") }} | {{ ghbadge("release-edge", "prometheus-scrape-target-k8s-operator") }} | (no libraries)                                                  |
| {{ repoentry("traefik-k8s-operator") }}                  | {{ ghbadge("release-edge", "traefik-k8s-operator") }}                  | {{ ghbadge("release-libs", "traefik-k8s-operator") }}           |
| {{ repoentry("traefik-route-k8s-operator") }}            | {{ ghbadge("release-edge", "traefik-route-k8s-operator") }}            | {{ ghbadge("release-libs", "traefik-route-k8s-operator") }}     |

| Bundle                             | Test Suite                             | Matrix Tests                               |
| ---------------------------------- | -------------------------------------- | ------------------------------------------ |
| {{ repoentry("cos-lite-bundle") }} | {{ ghbadge("ci", "cos-lite-bundle") }} | {{ ghbadge("matrix", "cos-lite-bundle") }} |

| Others                                                   | Release                                             |
| -------------------------------------------------------- | --------------------------------------------------- |
| {{ repoentry("cos-proxy-operator") }}                    | {{ ghbadge("release-edge", "cos-proxy-operator") }} |
| {{ repoentry("cos-tool", show_charmhub=False) }}         | {{ ghbadge("release", "cos-tool") }}                |
| {{ repoentry("observability-libs") }}                    | {{ ghbadge("release-libs", "observability-libs") }} |
| {{ repoentry("promql-transform", show_charmhub=False) }} | {{ ghbadge("release", "promql-transform") }}        |

{%
  include-markdown "../CHARMHUB_RELEASES.md"
%}

## Manual checks

To track the Charmhub release status, here's a useful bash script: 

```bash title="charmhub-summary.sh" linenums="1"
#!/usr/bin/env bash
# Produce a summary report of the Charmhub release status for all charms

charms="""
  alertmanager-k8s
  avalanche-k8s
  catalogue-k8s
  cos-configuration-k8s
  grafana-agent-k8s
  grafana-k8s
  karma-k8s
  loki-k8s
  observability-libs
  prometheus-k8s
  prometheus-scrape-config-k8s
  prometheus-scrape-target-k8s
  traefik-k8s
  traefik-route-k8s
"""

bundles="""
  cos-lite
"""

others="""
  cos-proxy
"""

# Make sure juju is installed
juju --version >/dev/null || (echo "Juju needs to be installed! (snap install juju)" && exit 1)
# Make sure yq is installed
yq --version >/dev/null || (echo "yq needs to be installed! (snap install yq)" && exit 1)

echo "# Charms\n"
for charm in ${charms}; do
  echo "## ${charm}" && juju info "${charm}" | yq .channels -r
done

echo "\n# Bundles\n"
for bundle in ${bundles}; do
  echo "## ${bundle}" && juju info "${bundle}" | yq .channels -r
done

echo "\n# Others\n"
for other in ${others}; do
  echo "## ${other}" && juju info "${other}" | yq .channels -r
done
```
