---
## Creating EC2 launch configuration.
- hosts: localhost
  connection: local
  gather_facts: False
  become: False

  vars:
    ami_id : "ami-06963965"
    ec2_group : "sap_ec2_sec_group"
    region : "ap-southeast-1"
    group : "default"
    instance_type : "t2.micro"
    snapShot : "snap-0e4ebb7174762f159"

  tasks:

    - name: Provisioning Launch configuration with name demolc
      local_action:
        module: ec2_lc
        name: demolc
        key_name: "common-ec2-keypair-2"
        security_groups: ["{{ ec2_group }}"]
        instance_type: "{{ instance_type }}"
        instance_profile_name: "ec2role"
        image_id: "{{ ami_id }}"
        region: "{{ region }}"
        assign_public_ip: "no"
        state: "present"
        #user data, it can be a shell scritp get executed once machine spin up.
        user_data: |
                  #!/bin/bash
                  yum update -y
                  yum remove java-1.7.0-openjdk -y
                  yum install java-1.8.0-openjdk.x86_64 -y
                  export AWS_ACCESS_KEY_ID=<changeme>
                  export AWS_SECRET_ACCESS_KEY=<changeme>
                  mkdir /opt/app
                  cd /opt/app
                  aws s3 cp s3://<BucketName>/vertx-web-1-1.0.tar vertx-web-1-1.0.tar
                  tar -xvf vertx-web-1-1.0.tar
                  cd vertx-web-1-1.0
                  ./bin/vertx-web-1

        volumes:
          - device_name: /dev/sdb
            snapshot: "{{ snapShot }}"
            volume_type: io1
            iops: 300
            volume_size: 10
            delete_on_termination: true
