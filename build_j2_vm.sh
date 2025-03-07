# In Exosphere (jetstream2.exosphere.app)
Go to https://jetstream2.exosphere.app/
Click Create -> Instance
Choose Rocky Linux 8 (same as used at MSI)
Name the instance something like GEMSX001
Choose m3.small (ensure enough RAM for Jupyter)
Select advanced
Select Assign a pulic IP address to this instance

# In OpenStack (js2.jetstream-cloud.org)
Go to https://js2.jetstream-cloud.org/project/instances/
On the drop down next to the new instance, choose "Edit Security Groups"
Add GEMSX001 to the instance\'s security groups

# Back in Exosphere
Open the list of instances
Note the attached IP address, referred to as INSTANCE-IP-ADDR below
Click the specific instance
Click the "Web Shell" Interactions

# Instance webshell
docker run -ti --privileged -p8888:8888 rockylinux:9 /bin/bash
dnf upgrade -y --refresh
dnf install -y dnf-plugins-core procps-ng

# Rocky 9 version
dnf config-manager --set-enabled crb
dnf install -y \
    https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
    https://dl.fedoraproject.org/pub/epel/epel-next-release-latest-9.noarch.rpm

dnf upgrade -y --refresh
dnf install -y slurm slurm-slurmctld slurm-slurmd vim sudo git zip which nano procps-ng ncurses openssh-clients wget
slurmd -C  
# Copy the output from above to /etc/slurmd/slurm.conf
# Update the partition info
create-munge-key
sudo -u munge munged
useradd jupyter
mkdir -p /opt/hpc4ag
chown jupyter /opt/hpc4ag
chgrp jupyter /opt/hpc4ag
sudo -u jupyter bash
cd /opt/hpc4ag 
wget https://s3.msi.umn.edu/hpc4ag/hpc4ag_data.tar.gz
tar -zxf hpc4ag_data.tar.gz
git clone https://github.com/GEMS-UMN/HPC4Ag.git /opt/hpc4ag/github_repo
cd /opt/hpc4ag/github_repo
/bin/bash ./build_venv.sh
source /opt/hpc4ag/venv/bin/activate
jupyter server password
jupyter lab --ip 0.0.0.0

