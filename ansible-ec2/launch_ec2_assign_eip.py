---
- name:  Example EC2 provisioning play
  hosts: localhost
  #connection: local
  gather_facts: False

  vars:
    ami_id : "ami-06963965"
    region : "ap-southeast-1"
    ec2_group : "sap_ec2_sec_group" 
    instance_type : "t2.micro" 
    key_pair: "common-ec2-keypair-2" 

  tasks:

    - name: Provisioning exactly one instance
      local_action:
        module: ec2
        key_name: "{{ key_pair }}"
        group: "{{ ec2_group }}"
        instance_type: "{{ instance_type }}"
        image: "{{ ami_id }}"
        region: "{{ region }}"
        vpc_subnet_id: "subnet-d00a65b4"
        wait: true
        assign_public_ip: "no"
        wait_timeout: 500
        volumes:
          - device_name: /dev/sdb
            snapshot: snap-0e4ebb7174762f159
            volume_type: io1
            iops: 300
            volume_size: 10
            delete_on_termination: true
        #count: 2
        exact_count: 1
        count_tag:
           Name: elb_bs
        instance_tags:
           Name: elb_bs
      register: ec2

    #### Assigning elastic ips to recently lauched ec2s.

    - name: Associate new elastic IP for each instance provisioned.
      local_action:
        module: ec2_eip
        region: "{{ region }}"
        device_id: "{{ item }}"
      with_items: "{{ ec2.instance_ids }}"

    #### debugging ec2 information.
    - name: Printing Ec2 information on console.
      local_action:
        module: debug
        msg:  "{{ item }}"
      ignore_errors: yes
      with_items: "{{ ec2.instances }}"

    #### Adding just lauched ec2 to host group, this can be used in later plays to perfom some actions on ec2s.
    - name: Adding new instance public ips to host group
      local_action:
        module: add_host
        hostname: "{{ item.public_ip }}"
        groupname: ec2hosts
      with_items: "{{ ec2.instances }}"

    #### Finally terminating instances created.
    - name: Finally terminate instances that were previously launched
      ec2:
        state: "absent"
        region: "{{ region }}"
        instance_ids: "{{ ec2.instance_ids }}"
