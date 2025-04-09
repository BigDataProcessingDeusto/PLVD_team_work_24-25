# Ansible script for deploying event generator for team work

1. On a root terminal install git and python3.*-venv. This procedure could change depending on your OS: 

```
$ sudo apt update && sudo apt install -y git python3.*-venv libffi-dev
```

1. Set AWS credentials at ~/.aws/credentials
2. Download SSH private key at ~/.ssh/vockey.pem
3. Set the proper permissions for the key: `chmod og-rwx ~/.ssh/vockey.pem`
4. Create a Python virtual environment: `python3 -m venv ~/ansible`
5. Activate the virtual environment: `source ~/ansible/bin/activate`
6. Clone the repository: `git clone https://github.com/BigDataProcessingDeusto/PLVD_team_work_24-25`
7. Access to `PLVD_team_work_24-25` directory: `cd PLVD_team_work_24-25`
8. Install requirements: `pip install -r requirements.txt`
9. Install event generator at AWS: `ansible-playbook -i inventory.aws_ec2.yml -u ec2-user --key-file=~/.ssh/vockey.pem deploy-event-generator.yml`
10. To access to HDFS NameNode UI, you must create another SSH tunnel: `ssh -i ~/.ssh/vockey.pem -N -L 8080:<master-node-public-name>:8080 ec2-user@<master-node-public-name>`
11. Kafka will be accessible from the Hadoop Cluster at <event-generator-private-ip>:9094


## Local deployment (for developing and testing purposes)

It is desirable that when you develop your scripts, to have a local working environment. You can launch the event-generator with the following command (docker and docker-compose is required):

```
$ docker-compose up --build
```

In some OS:

```
$ docker compose up --build
```
