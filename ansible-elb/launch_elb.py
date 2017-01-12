- name: Create Ec2 instance, Assign ElasticIP and Add to host group.
  hosts: localhost
  connection: local
  gather_facts: False
  #become: False

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
         assign_public_ip: "no"
         #count: 2
         exact_count: 1
         count_tag:
            Name: elb_bs
         instance_tags:
            Name: elb_bs
      register: ec2

    #### Assigning elastic ips to recently lauched ec2s.

    - name: associate new elastic IP for each instance.
      ec2_eip:
         region: "{{ region }}"
         device_id: "{{ item }}"
      with_items: "{{ ec2.instance_ids }}"

    #- name: Printing Ec2 information.
    #  debug:
    #    msg:  "{{ item }}"
    #  ignore_errors: yes
    #  with_items: "{{ ec2.instances }}"

    #### Adding just lauched ec2 to host group, this can be used in later plays to perfom some actions on ec2s.
    - name: Add new instance to host group
      add_host:
        hostname: "{{ item.private_ip }}"
        groupname: ec2hosts
      with_items: "{{ ec2.instances }}"

- name: Install Apache http
  hosts: ec2hosts
  sudo: yes

  tasks:
    - name: install apache2.
      apt: name=apache2 update_cache=yes state=latest

     #- name: Finally, terminate instances that were previously launched
     # ec2:
     #   state: "absent"
     #   region: "{{ region }}"
     #   instance_ids: "{{ ec2.instance_ids }}"

