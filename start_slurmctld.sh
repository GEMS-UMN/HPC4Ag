#!/bin/bash
sudo -u munge munged
slurmctld
slurmd
useradd -u 5555 jupyter
sudo -u jupyter /bin/bash
source /opt/hpc4ag/venv/bin/activate
cd /opt/hpc4ag/github_repo
jupyter lab --ip 0.0.0.0