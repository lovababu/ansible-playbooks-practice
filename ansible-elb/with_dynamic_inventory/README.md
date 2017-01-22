# Sample Playbook to
  - Launch EC2 ubuntu.
  - Create ELB and attach EC2 just launched.
  - Install Apache2 on EC2 just launched. 

launch_ec2_attachto_elb.py launches the EC2 and ELB, and attach EC2 to ELB.  
setup_apache_ec2.py make use of dynamic inventory to install the apache2 package on EC2s matched with tag Env=dev.  
 
##PreRequisites.  
  Set Your AWS account access and secret key as ENV variables   
  Create key pair.  
  Create Security group from console with in/outbound rules as mentioned below.    
    - Inbound: SSH with port 22, Http with port 80 enabled.  
    - Outbound: Open to anywhere.  
  
##How to Run?  
  Replace ```key_name``` , ```ec2_group``` and ```elb_group``` with you created.     
  Run the below commands from control machine.  
  ``` $ansible-playbook launch_ec2_attachto_elb.py --private-key <private key> -u ubuntu```  
  and then.
  ```$ansible-playbook -i ../../dynamic_inventory/ec2.py setup_apache_ec2.py --private-key <private key> -u ubuntu ```   
  
##Testing installation.  
  - Take ssh access of EC2 and verify the services running ($service --status-all), you must see apach2 service running.  
  - http://ELBDNSname:80/   --> Should show apache2 default page on browser.  
  
##Trouble Shooting.  
  It may failed with Permission denied, wrong public key  
   - Make sure you are using same key, was used to create EC2.  
  It may failed wit connection timed out.  
   - Make sure, SSH added in inbound rule of security group and you are able access through ssh.  
  It may failed during apach2 installation step.  
   - May be EC2 machine doesn't have internet access, check outbound rules.  
  http://ELBDNSName:80/ doesn't responding even playbook run successfully.  
   - Verify inbound rule, whether HTTP with 80 port rule added or not.  
   


 
 
