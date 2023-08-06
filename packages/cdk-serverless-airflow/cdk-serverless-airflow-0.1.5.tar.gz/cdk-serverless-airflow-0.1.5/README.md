# Serverless Airflow on AWS

[![Build](https://github.com/readybuilderone/serverless-airflow/actions/workflows/build.yml/badge.svg)](https://github.com/readybuilderone/serverless-airflow/actions/workflows/build.yml)

## Architecture

![architecture](./assets/01-serverless-airflow-on-aws-architecture.svg)

## Sample Code

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import cdk_serverless_airflow as airflow

app = cdk.App()
env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}
stack = cdk.Stack(app, "airflow-stack",
    env=env
)
airflow.Airflow(stack, "Airflow")
```

## Airflow Dashboard

![airflow-dashboard](./assets/04-airflow-dashboard.jpg)
