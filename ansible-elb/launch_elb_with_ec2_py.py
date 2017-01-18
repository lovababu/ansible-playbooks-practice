---
- name: Create Ec2 instance, Assign ElasticIP, Install Apache2 and add instance to elb.
  hosts: localhost
  user: ubuntu
  connection: local
  gather_facts: False
  become: False

  vars:
    ami_id : "ami-06963965"
    region : "ap-southeast-1"
    ec2_group : "sap_ec2_sec_group"
    elb_group : "sap_elb_sec_group"
    instance_type : "t2.micro" 

  tasks:

    - name: Provision exactly two instance
      ec2:
         key_name: "common-ec2-keypair"
         group: "{{ ec2_group }}"
         instance_type: "{{ instance_type }}"
         image: "{{ ami_id }}"
         region: "{{ region }}"
         wait: true
         assign_public_ip: no
         count: 2
         #exact_count: 2
         #count_tags:
         #   AppServer: elbbs
      register: ec2

    - name: Add tags to Ec2 instances.
      local_action:
        module: ec2_tag
        resource: "{{ item.id }}"
        region: "{{ region }}"
        state: "present"
        tags:
          Name: avoltest
          Env: dev
      with_items: "{{ ec2.instances }}"

    - name: associate new elastic IP for each instance.
      local_action:
        module: ec2_eip
        region: "{{ region }}"
        instance_id: "{{ item.id }}"
      with_items: "{{ ec2.instances }}"

    #- name: Wait for SSH to become available.
    #  pause: minutes=1

#Installing Apache 2 on Ec2s just launched, using dynamic inventory.
#- name: Install Apache2 on Ec2 just launched.
#  hosts: tag_Env_dev
#  user: ubuntu
#  gather_facts: True
#  become: True
#  tasks:
#    - name: install apache2.
#      apt: name=apache2 update_cache=yes state=latest
