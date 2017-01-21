# Command to ping remote server.  

##On Premise  
``` ansible -i hosts.ini all -m ping -u ubuntu```  

##Cloud  

If default Python as Interpretor:  

```$ansible -i <inventory> all -m raw -a 'sudo apt-get -y install python-simplejson' <privatekey> -u <user>```  

```$ansible -i <inventory> all -m ping --private-key <privatekey> -u <user> -e 'ansible_python_interpreter=/usr/bin/python' ```  

If Python3 as interpretor:  

```$ansible -i <inventory> all -m ping --private-key <privatekey> -u ubuntu -e 'ansible_python_interpreter=/usr/bin/python3' ```
 
 **before running the command update ec2_hosts.ini file accordingly**
 
##Trouble Shooting.  
If you encounter with /bin/sh: 1: /usr/bin/python: not found error.    
Solution: http://stackoverflow.com/questions/32429259/ansible-fails-with-bin-sh-1-usr-bin-python-not-found  



