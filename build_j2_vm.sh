# In Exosphere (jetstream2.exosphere.app)
# Go to https://jetstream2.exosphere.app/
# Click Create -> Instance
# Choose Rocky Linux 8 (same as used at MSI)
# Name the instance something like GEMSX001
# Choose m3.small (ensure enough RAM for Jupyter)
# Select advanced
# Select Assign a pulic IP address to this instance

# In OpenStack (js2.jetstream-cloud.org)
# Go to https://js2.jetstream-cloud.org/project/instances/
# On the drop down next to the new instance, choose "Edit Security Groups"
# Add GEMSX001 to the instance\'s security groups

# Back in Exosphere
# Open the list of instances
# Note the attached IP address, referred to as INSTANCE-IP-ADDR below
# Click the specific instance
# Click the "Web Shell" Interactions


# Create shared info
sudo /bin/bash
useradd -u 5555 jupyter
mkdir -p /opt/hpc4ag/etc
chown jupyter /opt/hpc4ag
chgrp jupyter /opt/hpc4ag
sudo -u jupyter bash
cd /opt/hpc4ag
wget https://s3.msi.umn.edu/hpc4ag/hpc4ag_data.tar.gz
tar -zxf hpc4ag_data.tar.gz
git clone https://github.com/GEMS-UMN/HPC4Ag.git /opt/hpc4ag/github_repo
cd /opt/hpc4ag/github_repo
git checkout dockerize
/bin/bash ./build_venv.sh
source /opt/hpc4ag/venv/bin/activate
jupyter server password
exit

# Instance webshell, build slurmdctld
docker run -ti --privileged --name slurm_ctld -v /home/jupyter:/home/jupyter -v /opt/hpc4ag:/opt/hpc4ag -v /opt/hpc4ag/etc/slurm:/etc/slurm --cpus 2 -p8888:8888 rockylinux:9 /bin/bash /opt/hpc4ag/build_slurmctld.sh

# build slurmd
docker run -ti --privileged --name slurm_worker1 -v /home/jupyter:/home/jupyter -v /opt/hpc4ag:/opt/hpc4ag -v /opt/hpc4ag/etc/slurm:/etc/slurm --cpus 2  rockylinux:9 /bin/bash /opt/hpc4ag/build_slurmd.sh

# Manipulate /opt/hpc4ag
