#!/usr/bin/env python3
import subprocess
import sys
from snakemd import Document, Table
import json
from datetime import datetime

CHARMS = [
    "alertmanager-k8s",
    "avalanche-k8s",
    "catalogue-k8s",
    "cos-configuration-k8s",
    "grafana-agent-k8s",
    "grafana-k8s",
    "karma-k8s",
    "loki-k8s",
    "observability-libs",
    "prometheus-k8s",
    "prometheus-scrape-config-k8s",
    "prometheus-scrape-target-k8s",
    "traefik-k8s",
    "traefik-route-k8s",
]

BUNDLES = [
    "cos-lite",
]

OTHERS = [
    "cos-proxy",
]

# Make sure juju is installed
status, result = subprocess.getstatusoutput("juju --version")
if status != 0:
    exit()

# Run juju info for all the charms and store information in a dict
charm_releases = {}
for charm in CHARMS:
    result = subprocess.run(["juju", "info", charm, "--format=json"], capture_output=True)
    charm_releases[charm] = json.loads(result.stdout)

bundle_releases = {}
for bundle in BUNDLES:
    result = subprocess.run(["juju", "info", bundle, "--format=json"], capture_output=True)
    bundle_releases[bundle] = json.loads(result.stdout)

other_releases = {}
for other in OTHERS:
    result = subprocess.run(["juju", "info", other, "--format=json"], capture_output=True)
    other_releases[other] = json.loads(result.stdout)
    


def _release_row(release_dict, charm, track):
    d = release_dict["channels"].get(track, [])

    def _version(channel):
        version = d[channel][0]['version'] if channel in d else '-'
        return version

    def _released_at(channel):
        if channel in d:
            original_date = d[channel][0]['released-at']
            original_format = '%Y-%m-%dT%H:%M:%S.%f+00:00'
            new_format = '^%Y-%m-%d\\ %H:%M^'
            return datetime.strptime(original_date, original_format).strftime(new_format)
        else:
            return '-'

    return [
        charm, 
        f"{_version('stable')}<br />{_released_at('stable')}",
        f"{_version('candidate')}<br />{_released_at('candidate')}",
        f"{_version('beta')}<br />{_released_at('beta')}",
        f"{_version('edge')}<br />{_released_at('edge')}",
    ]

def add_release_table(doc, releases_dict, track, title):
    doc.add_table(
        [title, f"{track}/stable", f"{track}/candidate", f"{track}/beta", f"{track}/edge"],
        [_release_row(release, charm, track) for charm, release in releases_dict.items()],
        [Table.Align.LEFT, Table.Align.CENTER, Table.Align.CENTER, Table.Align.CENTER, Table.Align.CENTER],
        indent=4
    )


doc = Document("CHARMHUB_RELEASES")

doc.add_header("Charmhub Releases", level=2)
doc.add_paragraph("These tables are updated by a script running periodically every hour, based on `juju info`. Times are in UTC (GMT+0).")
doc.add_paragraph('=== "latest"')
add_release_table(doc, charm_releases, "latest", "Charms")
add_release_table(doc, bundle_releases, "latest", "Bundles")
add_release_table(doc, other_releases, "latest", "Others")
doc.add_paragraph('=== "1.0"')
add_release_table(doc, charm_releases, "1.0", "Charms")
add_release_table(doc, bundle_releases, "1.0", "Bundles")
add_release_table(doc, other_releases, "1.0", "Others")
doc.output_page()

print(doc)
