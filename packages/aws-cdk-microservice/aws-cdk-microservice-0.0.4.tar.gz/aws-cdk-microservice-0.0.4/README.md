# aws-cdk-microservice

aws-cdk-microservice construct library is an open-source extension of the AWS Cloud Development Kit (AWS CDK) to deploy configurable microservice infra and its individual components in less than 50 lines of code and human readable configuration which can be managed by pull requests!

## A typical microservice architecture on AWS looks like:

![Architecture diagram](/static/microservice.png)

Using cdk a microservice can be deployed using the following sample code snippet:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_ec2 import SubnetType
from aws_cdk.core import Stack, StackProps
from constructs import Construct
from ...constructs.microservice import InfraEnv, MicroService, ProductName
from aws_cdk.core import App

class UnknownAPIStackDev(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        MicroService(stack, "UnknownAPI",
            app_name="UnknownAPI",
            env="development",
            asg_max_size="1",
            asg_min_size="1",
            disk_size=20,
            instance_labels=[{
                "key": "NODE-VERSION",
                "propagate_at_launch": True,
                "value": "12"
            }, {
                "key": "TYPE",
                "propagate_at_launch": True,
                "value": "application"
            }
            ],
            instance_type="t3.micro",
            vpc="vpc-1234567",
            port=8000,
            protocol="HTTP",
            health_check_path="/health",
            subnets=["subnet-987654321", "subnet-12345678"],
            tcp_rules=[{
                "source_sG": "sg-12345678",
                "description": "ssh rule",
                "port": 22
            }
            ],
            host="abc-test-123.smallcase.com",
            lb_arn="arn:aws:elasticloadbalancing:ap-south-1:12345678910:loadbalancer/app/API-DEV-External",
            ssl_enabled=False,
            ssh_key="master-dev",
            create_codedeploy_application=True,
            role={
                "type": "new"
            }
        )

UnknownAPIStackDev(app, "UnknownAPIStackDev",
    env=Environment(account="12345678910", region="ap-south-1")
)

app.synth()
```

Please refer [here](/API.md) to check how to use individual resource constructs.
