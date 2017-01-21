# Sample Playbook to install packages on existing Ubuntu EC2 machines.  

 - hosts.ini is inventory file, where we can group remote machines.  
 - install_apache2.py playbook contains task install apache2 server on hosts configured in hosts.ini file.  
 
##PreRequisites.  
  Set Your AWS account access and secret key as ENV variables   
  Launched EC2 machines using ```launch_ec2``` playbook, or from console.  
  key file (.pem) handy.
  EC2 machines security groups inbound and outbound rules adjusted as below.  
    - Inbound: SSH with port 22, Http with port 80 enabled.  
    - Outbound: Open to anywhere.  
  
##How to Run?  
  Open the hosts.ini file, and update the IP(EC2 public IPs) address accordingly.  
  
  Run the below commands from control machine.  
  ``` $ansible-playbook -i hosts.ini install_apache2.py --private-key <private key> -u ubuntu```   
  
##Testing installation.  
  - Take ssh access of EC2 and verify the services running ($service --status-all), you must see apach2 service running.  
  - http://EC2DNSname:80/   --> Should show apache2 default page on browser.  
  
##Trouble Shooting.  
  It may failed with Permission denied, wrong public key  
   - Make sure you are using same key, was used to create EC2.  
  It may failed wit connection timed out.  
   - Make sure, SSH added in inbound rule of security group and you are able access through ssh.  
  It may failed during apach2 installation step.  
   - May be EC2 machine doesn't have internet access, check outbound rules.  
  http://EC2DNSName:80/ doesn't responding even playbook run successfully.  
   - Verify inbound rule, whether HTTP with 80 port rule added or not.  
   


 
 
