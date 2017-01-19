- name: Install apache2 on existing Ec2 machine.
  hosts: ec2
  gather_facts: False
  become: True

  vars:
    region : "ap-southeast-1"

  tasks:

    - name: installing apache2.
      apt: name="{{ package_name }}" update_cache=yes state=latest
