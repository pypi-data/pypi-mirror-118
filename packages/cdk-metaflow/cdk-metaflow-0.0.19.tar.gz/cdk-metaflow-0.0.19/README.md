# CDK Metaflow

The `cdk-metaflow` package contains cdk constructs for deploying metaflow infrastructure on aws.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk_metaflow as metaflow
```

## Metaflow

The main construct creates all the required infrastructure for getting up and running with Metaflow on AWS. This is achieved by creating an instance of `Metaflow`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
metaflow = Metaflow(self, "metaflow")
```

Full example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_metaflow import Metaflow
import aws_cdk.core as cdk

class MetaflowStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        self.metaflow = Metaflow(self, "metaflow-ts")

dev_env = {
    "account": "123456789",
    "region": "us-west-2"
}

app = cdk.App()
MetaflowStack(app, "metaflow-stack-ts", env=dev_env)
```
