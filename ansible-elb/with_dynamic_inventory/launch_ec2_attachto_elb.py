---
- name: Play 1 creating two Ec2 instances.
  hosts: localhost
  user: ubuntu
  connection: local
  gather_facts: False
  become: False

  vars:
    ami_id : "ami-06963965"
    region : "ap-southeast-1"
    ec2_group : "sap_ec2_sec_group"
    instance_type : "t2.micro"

  tasks:

    - name: Provision exactly two instance
      local_action:
        module: ec2
        key_name: "common-ec2-keypair-2"
        group: "{{ ec2_group }}"
        instance_type: "{{ instance_type }}"
        image: "{{ ami_id }}"
        region: "{{ region }}"
        wait: true
        assign_public_ip: no
        vpc_subnet_id: "subnet-d00a65b4"
        count: 2
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

    - name: Add new instance to host group
      add_host:
        hostname: "{{ item.public_ip }}"
        groupname: ec2hosts
      with_items: "{{ ec2.instances }}"

    - name: Wait for SSH to come up
      wait_for:
        host: "{{ item.public_dns_name }}"
        port: 22
        delay: 60
        timeout: 320
        state: started
      with_items: "{{ ec2.instances }}"

## Play 2 Installing apache2 on Ec2, just launched.
- name: Play 2 Install Apache 2 on ec2hosts
  hosts: ec2hosts
  gather_facts: False
  become: True
  user: ubuntu
  pre_tasks:
    - name: 'install python2'
      raw: sudo apt-get -y install python-simplejson

  vars:
    region : "ap-southeast-1"
    package_name: "apache2"

  tasks:
    - name: installing apache2.
      apt: name="{{ package_name }}" update_cache=yes state=latest

## Play 3, Creating Elastic Ips and associating with Ec2 just launched.
- name: Play 3 Associate new elastice ips to ec2.
  hosts: localhost
  #connection: local
  gather_facts: False
  become: False

  vars:
    region: "ap-southeast-1"

  tasks:
    - name: Associate new elastic IP for each instance.
      local_action:
        module: ec2_eip
        region: "{{ region }}"
        instance_id: "{{ item.id }}"
      with_items: "{{ ec2.instances }}"

## Play 4 Creatin ELB and attaching Ec2 ids to ELB.
- name: Play 4 Creating ELB and attach Ec2.
  hosts: localhost
  #connection: local
  gather_facts: False
  become: False

  vars:
    region: "ap-southeast-1"
    elb_group: "sap_elb_sec_group"
    subnet_id: "subnet-d00a65b4"
  tasks:
    - name: Create ELB and attache Ec2 just launched.
      local_action:
        module: ec2_elb_lb
        name: "testelb"
        region: "{{ region }}"
        instance_ids: "{{ec2.instance_ids}}"
        security_group_names: 
           - "{{ elb_group }}"
        tags:
          Name: "test_elb"
        state: present
        subnets:
          - "{{ subnet_id }}"
        listeners: 
          - protocol: http
            load_balancer_port: 80
            instance_port: 80
            proxy_protocol: True
        health_check:
          ping_protocol: http # options are http, https, ssl, tcp
          ping_port: 80
          ping_path: "/" # not required for tcp or ssl
          response_timeout: 5 # seconds
          interval: 30 # seconds
          unhealthy_threshold: 2
          healthy_threshold: 10
