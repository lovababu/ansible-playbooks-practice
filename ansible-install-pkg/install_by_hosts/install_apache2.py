- name: Install apache2 on existing Ec2 machine.
  hosts: ec2
  gather_facts: True
  become: True
  pre_tasks:
    - name: 'Install python2 as pre task'
      raw: sudo apt-get -f -y install python-simplejson

  #vars:
  #  region : "ap-southeast-1"

  tasks:

    - name: installing apache2.
      apt: name="{{ package_name }}" update_cache=yes state=latest
