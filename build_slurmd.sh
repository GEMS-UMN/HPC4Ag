#!/bin/bash
dnf upgrade -y --refresh
dnf install -y dnf-plugins-core procps-ng
dnf config-manager --set-enabled crb
dnf install -y \
    https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
    https://dl.fedoraproject.org/pub/epel/epel-next-release-latest-9.noarch.rpm

dnf upgrade -y --refresh
dnf install -y slurm slurm-slurmd vim sudo git zip which nano procps-ng ncurses openssh-clients wget
slurmd -C | grep -v UpTime >> /etc/slurm/slurm.conf
tail -n 1 /etc/hosts >> /opt/hpc4ag/etc/hosts
cp /opt/hpc4ag/munge.key /etc/munge/
chown munge /etc/munge/munge.key
chgrp munge /etc/munge/munge.key
useradd -u 5555 jupyter 
exit
