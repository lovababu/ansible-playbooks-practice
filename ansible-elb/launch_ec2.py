- hosts: localhost
  connection: local
  gather_facts: False
  #become: False
  
  vars:
    ami_id : "ami-06963965"
    region : "ap-southeast-1"
    group : "default"
    state: "absent"
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
         count: 1
         #exact_count: 2
         count_tag:
            Name: ansible_ec2
         instance_tags:
            Name: ansible_ec2
      register: ec2

    - name: Printing Ec2 id & private ip.
      debug:
        msg: "Launched ec2 id {{ ec2.instances[0].id}} and private ip: {{ec2.instances[0].private_ip }}"

    #### Adding just lauched ec2 to host group, this can be used in later plays to perfom some actions on ec2s.
    #- name: Add new instance to host group
    #  add_host:
    #    hostname: "{{ item.public_ip }}"
    #    groupname: launched
    #  with_items: "{{ ec2.instances }}

    - name: Assign Elastic IP to Ec2.
      ec2_eip:
         device_id: "{{ ec2.instances[0].id }}"
         ip: 52.221.22.201
         region: "{{ region }}"
      register: instance_eip
      ignore_errors: yes
    - debug: var=instance_eip.public_ip

    - name: Terminate instances that were previously launched
      ec2:
        state: "{{ state }}"
        region: "{{ region }}"
        instance_ids: "{{ ec2.instance_ids }}"
