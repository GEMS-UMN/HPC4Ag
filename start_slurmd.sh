#!/bin/bash
cat /opt/hpc4ag/etc/hosts >> /etc/hosts
sudo -u munge munged
slurmd -D
