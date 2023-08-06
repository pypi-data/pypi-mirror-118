'''
# replace this
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
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_secretsmanager
import aws_cdk.core


class FlywayConstruct(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="flywaymigrationconstruct.FlywayConstruct",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        migration_bucket_secret_manager: aws_cdk.aws_secretsmanager.ISecret,
        security_groups: typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup],
        subnet: aws_cdk.aws_ec2.SubnetSelection,
        vpc: aws_cdk.aws_ec2.IVpc,
        memory_size: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: 
        :param migration_bucket_secret_manager: 
        :param security_groups: 
        :param subnet: 
        :param vpc: 
        :param memory_size: 
        :param timeout: 
        '''
        params = FlywayConstructParams(
            bucket=bucket,
            migration_bucket_secret_manager=migration_bucket_secret_manager,
            security_groups=security_groups,
            subnet=subnet,
            vpc=vpc,
            memory_size=memory_size,
            timeout=timeout,
        )

        jsii.create(FlywayConstruct, self, [scope, id, params])

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="BUCKET_CODE_ARN")
    def BUCKET_CODE_ARN(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "BUCKET_CODE_ARN"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="HANDLER")
    def HANDLER(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "HANDLER"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ID_LAMBDA_CODE")
    def ID_LAMBDA_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ID_LAMBDA_CODE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="OBJECT_CODE_KEY")
    def OBJECT_CODE_KEY(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "OBJECT_CODE_KEY"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="flywayLambdaMigration")
    def flyway_lambda_migration(self) -> aws_cdk.aws_lambda.Function:
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "flywayLambdaMigration"))

    @flyway_lambda_migration.setter
    def flyway_lambda_migration(self, value: aws_cdk.aws_lambda.Function) -> None:
        jsii.set(self, "flywayLambdaMigration", value)


@jsii.data_type(
    jsii_type="flywaymigrationconstruct.FlywayConstructParams",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "migration_bucket_secret_manager": "migrationBucketSecretManager",
        "security_groups": "securityGroups",
        "subnet": "subnet",
        "vpc": "vpc",
        "memory_size": "memorySize",
        "timeout": "timeout",
    },
)
class FlywayConstructParams:
    def __init__(
        self,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        migration_bucket_secret_manager: aws_cdk.aws_secretsmanager.ISecret,
        security_groups: typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup],
        subnet: aws_cdk.aws_ec2.SubnetSelection,
        vpc: aws_cdk.aws_ec2.IVpc,
        memory_size: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''
        :param bucket: 
        :param migration_bucket_secret_manager: 
        :param security_groups: 
        :param subnet: 
        :param vpc: 
        :param memory_size: 
        :param timeout: 
        '''
        if isinstance(subnet, dict):
            subnet = aws_cdk.aws_ec2.SubnetSelection(**subnet)
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "migration_bucket_secret_manager": migration_bucket_secret_manager,
            "security_groups": security_groups,
            "subnet": subnet,
            "vpc": vpc,
        }
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def migration_bucket_secret_manager(self) -> aws_cdk.aws_secretsmanager.ISecret:
        result = self._values.get("migration_bucket_secret_manager")
        assert result is not None, "Required property 'migration_bucket_secret_manager' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def security_groups(self) -> typing.List[aws_cdk.aws_ec2.ISecurityGroup]:
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[aws_cdk.aws_ec2.ISecurityGroup], result)

    @builtins.property
    def subnet(self) -> aws_cdk.aws_ec2.SubnetSelection:
        result = self._values.get("subnet")
        assert result is not None, "Required property 'subnet' is missing"
        return typing.cast(aws_cdk.aws_ec2.SubnetSelection, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlywayConstructParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FlywayConstruct",
    "FlywayConstructParams",
]

publication.publish()
