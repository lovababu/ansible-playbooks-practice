---
- name: Install apache2 on existing Ec2 machine by tag name.
  hosts: tag_Env_dev
  gather_facts: False
  user: ubuntu
  become: True
  pre_tasks:
    - name: 'Install python2 as pre task'
      raw: sudo apt-get -y install python-simplejson

  vars:
    region : "ap-southeast-1"
    package_name: "apache2"
  tasks:

    - name: Installing apache2.
      apt: name="{{ package_name }}" update_cache=yes state=latest

    - name: Replace index.html in /var/www/html
      copy:
        src: index.html
        dest: /var/www/html/index.html
        owner: root
        group: root

    #- name: uninstalling apache2.
    #  apt: name="{{ package_name }}" state=removed
