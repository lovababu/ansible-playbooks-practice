## Command to ping remote server.

``` ansible -i ec2_ping.ini all -m ping --private-key /root/common-ec2-keypair-2.pem  -u ubuntu```

 **before running the command update ec2_hosts.ini file accordingly**
