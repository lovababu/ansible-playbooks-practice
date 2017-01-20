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
        image_id: "{{ ami_id }}"
        region: "{{ region }}"
        assign_public_ip: "no"
        state: "present"
        volumes:
          - device_name: /dev/sdb
            snapshot: "{{ snapShot }}"
            volume_type: io1
            iops: 300
            volume_size: 10
            delete_on_termination: true
        #user data, it can be a shell scritp get executed once machine spin up.
        user_data: |
                   #!/bin/bash 
                   sudo apt-get update 
                   sudo apt-get install apache2 
                   hostname=$(hostname -f) 
                   echo '<h3>I am the instance $hostname</h3>' > /var/www/html/index.html
