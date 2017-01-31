---
## Creating EC2 launch configuration and attaching to asg.
- hosts: localhost
  connection: local
  gather_facts: False
  become: False

  vars:
    ami_id : "ami-4dd6782e"
    ec2_group : "sg-628d5505"
    region : "ap-southeast-1"
    group : "default"
    instance_type : "t2.micro"
    snapShot : "snap-0e4ebb7174762f159"

    lc_name: "vertxlc"
    asg_name: "vertxasg"
    elb_name: "vertxelb"
    elb_group: "sap_elb_sec_group"
    subnet_id: "subnet-d00a65b4"

  tasks:

    - name: Provisioning Launch configuration with name demolc
      local_action:
        module: ec2_lc
        name: "{{ lc_name }}"
        key_name: "common-ec2-keypair-2"
        security_groups: ["{{ ec2_group }}"]
        instance_type: "{{ instance_type }}"
        image_id: "{{ ami_id }}"
        region: "{{ region }}"
        assign_public_ip: "yes"
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
                  yum update -y
                  yum remove java-1.7.0-openjdk -y
                  yum install java-1.8.0-openjdk.x86_64 -y
                  export AWS_ACCESS_KEY_ID=<ChangeMe>
                  export AWS_SECRET_ACCESS_KEY=<ChangeMe>
                  mkdir /opt/app
                  cd /opt/app
                  cd /opt/app
                  aws s3 cp s3://avol-deliverables/vertx-web-1-1.0.tar vertx-web-1-1.0.tar
                  tar -xvf vertx-web-1-1.0.tar
                  cd vertx-web-1-1.0
                  ./bin/vertx-web-1

    ## Create ELB.
    - name: Creating Elastic Load Balancer.
      local_action:
        module: ec2_elb_lb
        name: "{{ elb_name }}"
        region: "{{ region }}"
        security_group_names:
           - "{{ elb_group }}"
        tags:
          Name: "Dev"
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

    #Create ASG and attache ELB.
    - name: Creating AutoScaling Group with Launch configuration demolc
      local_action:
        module: ec2_asg
        name: "{{ asg_name }}"
        launch_config_name: "{{ lc_name }}"
        region: "{{ region }}"
        vpc_zone_identifier: ["{{ subnet_id }}"]
        health_check_period: 300
        health_check_type: ELB
        min_size: 1
        max_size: 2
        desired_capacity: 2
        availability_zones: ["ap-southeast-1a"]
        load_balancers: ["{{ elb_name }}"]
        wait_timeout: 500
