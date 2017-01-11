- hosts: localhost
  connection: local
  gather_facts: False
  become: False
  
  vars:
    ami_id : "ami-06963965"
    region : "ap-southeast-1"
    group : "default"
    instance_type : "t2.micro" 
  tasks:

    - name: Provision exactly on instance
      ec2:
         key_name: "common-ec2-keypair"
         group: "{{ group }}"
         instance_type: "{{ instance_type }}"
         image: "{{ ami_id }}"
         region: "{{ region }}"
         wait: true
         exact_count: 2
         count_tag:
            Name: Demo
         instance_tags:
            Name: Qa
      register: ec2
