---
title: Status
summary: A page with the status of Canonical's Observability repos.
author: Luca Bello
date: 2023-01-25
---
# Status

This page contains the current status of all the charms managed by the Observability team.

## Charms

| Charm                                                    | Release Charm                                                          | Release Libraries                                                      |
| -------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| {{ repoentry("alertmanager-k8s-operator") }}             | {{ ghbadge("release-edge", "alertmanager-k8s-operator") }}             | {{ ghbadge("release-libs", "alertmanager-k8s-operator") }}             |
| {{ repoentry("avalanche-k8s-operator") }}                | {{ ghbadge("release-edge", "avalanche-k8s-operator") }}                | {{ ghbadge("release-libs", "avalanche-k8s-operator") }}                |
| {{ repoentry("catalogue-k8s-operator") }}                | {{ ghbadge("release-edge", "catalogue-k8s-operator") }}                | {{ ghbadge("release-libs", "catalogue-k8s-operator") }}                |
| {{ repoentry("cos-configuration-k8s-operator") }}        | {{ ghbadge("release-edge", "cos-configuration-k8s-operator") }}        | {{ ghbadge("release-libs", "cos-configuration-k8s-operator") }}        |
| {{ repoentry("grafana-agent-k8s-operator") }}            | {{ ghbadge("release-edge", "grafana-agent-k8s-operator") }}            | {{ ghbadge("release-libs", "grafana-agent-k8s-operator") }}            |
| {{ repoentry("grafana-k8s-operator") }}                  | {{ ghbadge("release-edge", "grafana-k8s-operator") }}                  | {{ ghbadge("release-libs", "grafana-k8s-operator") }}                  |
| {{ repoentry("karma-k8s-operator") }}                    | {{ ghbadge("release-edge", "karma-k8s-operator") }}                    | {{ ghbadge("release-libs", "karma-k8s-operator") }}                    |
| {{ repoentry("loki-k8s-operator") }}                     | {{ ghbadge("release-edge", "loki-k8s-operator") }}                     | {{ ghbadge("release-libs", "loki-k8s-operator") }}                     |
| {{ repoentry("observability-libs") }}                    | {{ ghbadge("release-edge", "observability-libs") }}                    | {{ ghbadge("release-libs", "observability-libs") }}                    |
| {{ repoentry("prometheus-k8s-operator") }}               | {{ ghbadge("release-edge", "prometheus-k8s-operator") }}               | {{ ghbadge("release-libs", "prometheus-k8s-operator") }}               |
| {{ repoentry("prometheus-scrape-config-k8s-operator") }} | {{ ghbadge("release-edge", "prometheus-scrape-config-k8s-operator") }} | {{ ghbadge("release-libs", "prometheus-scrape-config-k8s-operator") }} |
| {{ repoentry("prometheus-scrape-target-k8s-operator") }} | {{ ghbadge("release-edge", "prometheus-scrape-target-k8s-operator") }} | {{ ghbadge("release-libs", "prometheus-scrape-target-k8s-operator") }} |
| {{ repoentry("traefik-k8s-operator") }}                  | {{ ghbadge("release-edge", "traefik-k8s-operator") }}                  | {{ ghbadge("release-libs", "traefik-k8s-operator") }}                  |
| {{ repoentry("traefik-route-k8s-operator") }}            | {{ ghbadge("release-edge", "traefik-route-k8s-operator") }}            | {{ ghbadge("release-libs", "traefik-route-k8s-operator") }}            |

## Bundles

| Bundle                             | Test Suite                             | Matrix Tests                               |
| ---------------------------------- | -------------------------------------- | ------------------------------------------ |
| {{ repoentry("cos-lite-bundle") }} | {{ ghbadge("ci", "cos-lite-bundle") }} | {{ ghbadge("matrix", "cos-lite-bundle") }} |

## Others

| Others                                                   | Release                                             |
| -------------------------------------------------------- | --------------------------------------------------- |
| {{ repoentry("cos-proxy-operator") }}                    | {{ ghbadge("release-edge", "cos-proxy-operator") }} |
| {{ repoentry("cos-tool", show_charmhub=False) }}         | {{ ghbadge("release", "cos-tool") }}                |
| {{ repoentry("promql-transform", show_charmhub=False) }} | {{ ghbadge("release", "promql-transform") }}        |
