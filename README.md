# To Deploy test env pls exec py script
```
python ./deploy.py --EnvironmentName test1 --DeployELB true
```
* --EnvironmentName default is test1. Can be changed to any [a-z]+[0-1] name but be awere on CFN limitation for params.
* --DeployELB default is true. Can be true of false. If false only VPC will be created without ELB and DNS records!!!