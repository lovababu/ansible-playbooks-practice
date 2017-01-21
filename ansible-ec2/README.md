# Sample Playbook to launch EC2 machine and Assign Elastic IP.

 - launch_ec2.py playbook launch the exactly 2 Ec2 machines with ubuntu AMI.  
 - launch_ec2_assign_eip.py playbook Launches the exactly 2 EC2 machines with ubuntu AMI and Assign new Elastic IPs to the EC2s.  
 
##PreRequisites.  
  Your AWS account access and secret key as ENV variables   
  Create a Key Pair from EC2 dash board, and download the key.
 
##How to Run?  
  Open the launch_ec2.py, and change **key_name** with the key pair name you have created.  
  Adjust the **exact_count** to launch no of instances.  
  Change **region**, if required.
  
  Run the below commands from control machine.  
  ``` $ansible-playbook launch_ec2.py ```  
  ``` $ansible-playbook launch_ec2_assign_eip.py ```  
  
  **Once EC2's launched adjust the security groups if required, since we are launching with default security group here.**
  
**Note:** Free tier users cannot launch more than 2 running instances.  