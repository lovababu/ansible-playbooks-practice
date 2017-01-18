---
- name: Gethering Ec2 facts.
  hosts: all
  gather_facts: True
  user: ubuntu

  tasks:
    #- name: gethering facts of Ec2 by tag.
    #  local_action:
    #    module: ec2_facts
    #  register: ec2facts

    #- debug: var=ec2facts
    - name: Gather facts
      ec2_facts:

    - name: Conditional
      debug:
        msg: "This instance is a t1.micro"
      when: ansible_ec2_instance_type == "t2.micro"
    
