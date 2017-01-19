---
- name: Install apache2 on existing Ec2 machine by its tag.
  hosts: tag_Env_dev
  gather_facts: True
  user: ubuntu
  become: True

  vars:
    region : "ap-southeast-1"
    package_name: "apache2"

  tasks:

    - name: Installing apache2 on EC2.
      apt: name="{{ package_name }}" update_cache=yes state=latest

    ## Uninstalling specific package.
    #- name: Uninstalling apache2.
    #  apt: name="{{ package_name }}" state=removed
