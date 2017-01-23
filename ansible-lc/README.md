# Sample playbook to create Launch Configuration and attach to AutoScalingGroup.

 - launch_lc.py playbook creates the launch configuration.  
 - launch_asg.py playbook creates the launch configuration, auto scaling group, Load balancer and attach LC and ELB to Auto scaling group.  

 ## Prerequisites.
  - Set Your AWS account access and secret key as ENV variables   
  - Create key pair.  
  - Create two Security group(one for Ec2, another for ELB) from console with in/outbound rules as mentioned below.    
    - Inbound: SSH with port 22, Http with port 80 enabled.  
    - Outbound: Open to anywhere.  

 ## How to Run?
   Replace ```key_name``` , ```ec2_group``` and ```elb_group``` with you created.       
   Replace Access key/Secret key (find ```<changeme>``` and replace)  
   Upload **vertx-web-1.1.0.tar** to S3 bucket.  
   Replace ```<BucketName>``` with your bucket name.  
   Run the below commands from control machine to create launch configuration and assign it asg from console.    
   ``` $ansible-playbook launch_lc.py ```    

   Run the below command from control machine to create LaunchConfiguration, Auto Scaling Group and ELB.  
   ```$ansible-playbook launch_asg.py ```

 ## How to Test?  
   If playbook runs successfully.  
   Open ELB and check the status of EC2 machines, it should be in **InService**.  
   Open Browser and point to http://<ELB DNS Name>:80/ , you must recieve json with ec2 ip.  
  