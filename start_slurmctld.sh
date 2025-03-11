#!/bin/bash
cat /opt/hpc4ag/etc/hosts >> /etc/hosts
sudo -u munge munged
slurmctld
slurmd
sudo -u jupyter /bin/bash
source /opt/hpc4ag/venv/bin/activate
cd /opt/hpc4ag/github_repo
jupyter lab --ip 0.0.0.0