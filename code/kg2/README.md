# Where to download the RTX KG2 knowledge graph

http://rtx-kg2-public.s3-website-us-west-2.amazonaws.com/

# How to build your own RTX KG2

## General notes:

The KG2 build system is designed only to run in an Ubuntu 18.04 environment
(i.e., either (i) an Ubuntu 18.04 host OS or (ii) Ubuntu 18.04 running in a
Docker container with a host OS that has `bash` and `sudo`). Currently, KG2 is
built using a set of `bash` scripts that are designed to run in Amazon's Elastic
Compute Cloud (EC2), and thus, configurability and/or coexisting with other
installed software pipelines was not a design consideration for the build
system. The KG2 build system's `bash` scripts create three subdirectories
`~/kg2-build`, `~/kg2-code`, and `~/kg2-venv` under the `${HOME}` directory of
whatever Linux user account you use to run the KG2 build software (if you run on
an EC2 Ubuntu instance, this directory would by default be `/home/ubuntu`). The
various directories used by the KG2 build system are configured in the `bash`
include file `master-config.shinc`.

Note about atomicity of file moving: The build software is designed to run with
the `kg2-build` directory being in the same file system as the Python temporary
file directory (i.e., the directory name that is returned by the variable
`tempfile.tempdir` in Python). If you modify the KG2 software or runtime
environment so that `kg2-build` is in a different file system from the file
system in which the directory `tempfile.tempdir` resides, then the file moving
operations that are performed by the KG2 build software will not be atomic and
interruption of `build-kg2.py` could then leave a source data file in a
half-downloaded (i.e., broken) state.

## Setup your computing environment

The computing environment where you will be running the KG2 build should be
running Ubuntu 18.04.  Your build environment should have the following *minimum*
specifications:

- 488 GiB of system memory
- 1,023 GiB of disk space in the root file system 
- high-speed networking (20 Gb/s networking) and storage
- ideally, AWS zone `us-west-2` since that is where the RTX KG2 S3 buckets are located

## The KG2 build system assumes there is no MySQL database already present

The target Ubuntu system in which you will run the KG2 build should *not* have MySQL
installed; if MySQL is installed, you will need to delete it using the following
`bash` command, which requires `curl`: (WARNING! Please don't run this command
without first making a backup image of your system, such as an AMI):

    source <(curl -s https://raw.githubusercontent.com/RTXteam/RTX/master/code/kg2/delete-mysql-ubuntu.sh)

The KG2 build system has been tested *only* under Ubuntu 18.04. If you want to
build KG2 but don't have a native installation of Ubuntu 18.04 available, your
best bet would be to use Docker (see Option 3 below). 

## AWS authentication key and AWS buckets

Aside from your host OS, you'll need to have an Amazon Web Services (AWS)
authentication key that is configured to be able to read from the `s3://rtx-kg2`
Amazon Simple Cloud Storage Service (S3) bucket (ask Stephen Ramsey to set this
up), so that the build script can download a copy of the full Unified Medical
Language System (UMLS) distribution.  You will be asked (by the AWS Command-line
Interface, CLI) to provide this authentication key when you run the KG2 build
script. Your configured AWS CLI will also need to be able to programmatically
write to the (publicly readable) S3 bucket `s3://rtx-kg2-public` (both buckets
are in the `us-west-2` AWS zone). The KG2 build script downloads the UMLS
distribution (including SNOMED CT) from the private S3 bucket `rtx-kg2` (IANAL,
but it appears that UMLS is encumbered by a license preventing redistribution so
I have not hosted them on a public server for download; but you can get it for
free at the [UMLS website](https://www.nlm.nih.gov/research/umls/) if you agree
to the UMLS licenses) and it uploads the final output `kg2.json.gz` file to the
public S3 bucket `rtx-kg2-public`. Alternatively, you can set up your own S3
bucket to which to copy the gzipped KG2 JSON file, or you can comment the line
out of `build-kg2.sh` that copies the final gzipped JSON file to S3.

## My normal EC2 instance

The KG2 build software has been tested with the following instance type:

- AMI: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - `ami-005bdb005fb00e791` (64-bit x86)
- Instance type: `r4.16xlarge` (488 GiB of memory)
- Storage: 1,023 GiB General Purpose SSD
- Security Group: ingress TCP packets on port 22 (ssh) permitted

As of June 10, 2019, an on-demand `r4.16xlarge` instance in the `us-west-2` AWS
zone costs $4.26 per hour, so the cost to build KG2 (estimated to take 48 hours)
would be approximately $200 (this is currently just a rough estimate, plus or
minus 20%). [Unfortunately, AWS doesn't seem to allow the provisioning of spot
instances while specifying minimum memory greater than 240 GiB; but perhaps soon
that will happen, and if so, it could save significantly on the cost of building KG2.]

## Build instructions

Note: to follow the instructions for Option 2 and Option 3 below, you will need
to be using the `bash` shell on your local computer.

### Option 1: build KG2 directly on an Ubuntu system:

These instructions assume that you are logged into the target Ubuntu system:

(1) Install `git` by running this command in the `bash` shell:

    sudo apt-get update -y && sudo apt-get install -y screen git

(2) change to the user's home directory:

    cd 
    
(3) Clone the RTX software from GitHub:

    git clone https://github.com/RTXteam/RTX.git

(4) Setup the KG2 build system: 

    RTX/code/kg2/setup-kg2.sh

Note that there is no need to redirect `stdout` or `stderr` to a log file, when
executing `setup-kg2.sh`; this is because the script saves its own `stdout` and
`stderr` to a log file `/home/ubuntu/setup-kg2.log`.

(5) Look in the log file `/home/ubuntu/setup-kg2.sh` to see if the script
completed successfully; it should end with `======= script finished ======`.

(6) Initiate a `screen` session to provide a stable pseudo-tty:

    screen

(7) Within the `screen` session, run:

    bash -x ~/kg2-code/build-kg2.sh all

Then exit screen (`ctrl-a d`). Note that there is no need to redirect `stdout`
or `stderr` to a log file, when executing `build-kg2.sh`; this is because the
script saves its own `stdout` and `stderr` to a log file `build-kg2.log`. You can
watch the progress of your KG2 build by using this command:

    tail -f ~/kg2-build/build-kg2.log
    
Note that the `build-multi-owl-kg.sh` script also saves `stderr` from running `multi_owl_to_json_kg.py`
to a file `~/kg2-build/build-kg2-owl-stderr.log`.

### Option 2: remotely build KG2 in an EC2 instance via ssh, orchestrated from your local computer

This option requires that you have `curl` installed on your local computer. In a
`bash` terminal session, set up the remote EC2 instance by running this command
(requires `ssh` installed and in your path):

    source <(curl -s https://raw.githubusercontent.com/RTXteam/RTX/master/code/kg2/ec2-setup-remote-instance.sh)
    
You will be prompted to enter the path to your AWS PEM file and the hostname of
your AWS instance.  The script should then initiate a `bash` session on the
remote instance. Within that `bash` session, continue to follow the instructions
for Option 1.

### Option 3: in an Ubuntu container in Docker (UNTESTED, IN DEVELOPMENT)

(1) If you are on Ubuntu and you need to install Docker, you can run this command in `bash` on the host OS:
   
    source <(curl -s https://raw.githubusercontent.com/RTXteam/RTX/master/code/kg2/install-docker.sh)
    
(otherwise, the subsequent commands in this section assume that Docker is installed
on whatever host OS you are running). 

(2) Clone the RTX software into your home directory:

    cd 
    
    git clone https://github.com/RTXteam/RTX.git

(3) Build a Docker image for KG2:
    
    sudo docker build -t kg2 RTX/code/kg2/
    
(4) Setup a container and setup KG2 in it:

    sudo docker run -it --name kg2 kg2:latest su - ubuntu -c "RTX/code/kg2/setup-kg2.sh"
    
(If anything goes wrong, look for an error message using `sudo docker exec kg2 "cat setup-kg2.log"`)

(5) Set up a persistent pseudo-tty using `screen`:

    screen
    
(6) Inside the `screen` session, run:
    
    sudo docker exec kg2 "bash -x kg2-code/build-kg2.sh all"

Then exit screen (`ctrl-a d`). You can watch the progress of your KG2 setup using the
following command:

    sudo docker exec -it kg2 "tail -f kg2-build/build-kg2.log"

Note that the `build-multi-owl-kg.sh` script also saves `stderr` from running `multi_owl_to_json_kg.py`
to a file `~/kg2-build/build-kg2-owl-stderr.log` inside the container.

## The output KG

The `build-kg2.sh` script (run via one of the three methods shown above) creates
a JSON file `kg2.json.gz` and copies it to a publicly accessible S3 bucket
`rtx-kg2-public`. You can access the gzipped JSON file via HTTP, as shown here:

    curl https://s3-us-west-2.amazonaws.com/rtx-kg2-public/kg2.json.gz > kg2.json.gz

Or using the AWS command-line interface (CLI) tool `aws` with the command

    aws s3 cp s3://rtx-kg2-public/kg2.json.gz .

You can access the various artifacts from the KG2 build (config file, log file,
etc.) at the AWS static website endpoint for the 
`rtx-kg2-public` S3 bucket: <http://rtx-kg2-public.s3-website-us-west-2.amazonaws.com/>
