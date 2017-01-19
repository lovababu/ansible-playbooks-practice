---
- name: Gethering the remote host facts.
  hosts: ec2hosts
  user: ubuntu
  gather_facts: False
  become: True
  pre_tasks:
    - name: 'install python2'
      raw: sudo apt-get -y install python-simplejson

  tasks:

    - ec2_remote_facts:
        filters:
          instance-state-name: running
          "tag:Env": "Dev"
      register: ec2hosts


    - debug: var=ec2hosts
