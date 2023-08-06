'''
[![Build](https://github.com/readybuilderone/serverless-airflow/actions/workflows/build.yml/badge.svg)](https://github.com/readybuilderone/serverless-airflow/actions/workflows/build.yml)
[![NPM version](https://badge.fury.io/js/cdk-serverless-airflow.svg)](https://badge.fury.io/js/cdk-serverless-airflow)
[![PyPI version](https://badge.fury.io/py/cdk-serverless-airflow.svg)](https://badge.fury.io/py/cdk-serverless-airflow)

# `CDK Serverless Airflow`

CDK construct library that allows you to create [Apache Airflow](https://airflow.apache.org/) on AWS in TypeScript or Python

# Architecture

![architecture](./assets/01-serverless-airflow-on-aws-architecture.svg)

# Sample

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

# Airflow Dashboard

> Default Credential: user/bitnami

![airflow-dashboard](./assets/04-airflow-dashboard.jpg)

# AWS China Regions

AWS China regions `cn-north-1` and `cn-northwest-1` are supported by this Library.

## License

This project is licensed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.core


class Foo(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-serverless-airflow.Foo",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: 
        '''
        props = FooProps(vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))


@jsii.data_type(
    jsii_type="cdk-serverless-airflow.FooProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class FooProps:
    def __init__(self, *, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None) -> None:
        '''
        :param vpc: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FooProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Foo",
    "FooProps",
]

publication.publish()
