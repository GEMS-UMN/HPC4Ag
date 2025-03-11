#!/bin/bash
cat /opt/hpc4ag/etc/hosts >> /etc/hosts
sudo -u munge munged
slurmctld
slurmd
cd /opt/hpc4ag/github_repo
sudo -u jupyter /opt/hpc4ag/venv/bin/jupyter lab --ip 0.0.0.0 --ServerApp.root_dir /opt/hpc4ag/github_repo/ 