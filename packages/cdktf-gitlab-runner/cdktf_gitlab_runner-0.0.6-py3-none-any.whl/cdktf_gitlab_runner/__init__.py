'''
[![NPM version](https://badge.fury.io/js/cdktf-gitlab-runner.svg)](https://badge.fury.io/js/cdktf-gitlab-runner)
[![PyPI version](https://badge.fury.io/py/cdktf-gitlab-runner.svg)](https://badge.fury.io/py/cdktf-gitlab-runner)
![Release](https://github.com/neilkuan/cdktf-gitlab-runner/workflows/release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdktf-gitlab-runner?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdktf-gitlab-runner?label=pypi&color=blue)

# Welcome to `cdktf-gitlab-runner`

Use CDK fo Terraform to create gitlab runner, and use [gitlab runner](https://gitlab.com/gitlab-org/gitlab-runner) to help you execute your Gitlab Pipeline Job.

> GitLab Runner is the open source project that is used to run your CI/CD jobs and send the results back to GitLab. [(source repo)](https://gitlab.com/gitlab-org/gitlab-runner)

### Init CDKTF Project

```bash
mkdir demo
cd demo
cdktf init --template typescript --local
```

### Install `cdktf-gitlab-runner`

```bash
yarn add cdktf-gitlab-runner
or
npm i cdktf-gitlab-runner
```

### Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdktf_cdktf_provider_google as gcp
import cdktf as cdktf
from constructs import Construct
from ..index import GitlabRunnerAutoscaling

class IntegDefaultStack(cdktf.TerraformStack):
    def __init__(self, scope, id):
        super().__init__(scope, id)
        local = "asia-east1"
        project_id = f"{process.env.PROJECT_ID}"
        provider = gcp.GoogleProvider(self, "GoogleAuth",
            region=local,
            zone=local + "-c",
            project=project_id
        )
        GitlabRunnerAutoscaling(self, "GitlabRunnerAutoscaling",
            gitlab_token=f"{process.env.GITLAB_TOKEN}",
            provider=provider
        )

app = cdktf.App()
IntegDefaultStack(app, "gitlab-runner")
app.synth()
```
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

import cdktf_cdktf_provider_google
import constructs


@jsii.data_type(
    jsii_type="cdktf-gitlab-runner.DockerVolumes",
    jsii_struct_bases=[],
    name_mapping={"container_path": "containerPath", "host_path": "hostPath"},
)
class DockerVolumes:
    def __init__(
        self,
        *,
        container_path: builtins.str,
        host_path: builtins.str,
    ) -> None:
        '''Docker Volumes interface.

        :param container_path: Job Runtime Container Path Host Path.
        :param host_path: EC2 Runner Host Path.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "container_path": container_path,
            "host_path": host_path,
        }

    @builtins.property
    def container_path(self) -> builtins.str:
        '''Job Runtime Container Path Host Path.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            -/tmp/cahce
            moredetailseehttps:
        '''
        result = self._values.get("container_path")
        assert result is not None, "Required property 'container_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_path(self) -> builtins.str:
        '''EC2 Runner Host Path.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            -/tmp/cahce
            moredetailseehttps:
        '''
        result = self._values.get("host_path")
        assert result is not None, "Required property 'host_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitlabRunnerAutoscaling(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-gitlab-runner.GitlabRunnerAutoscaling",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        gitlab_token: builtins.str,
        provider: cdktf_cdktf_provider_google.GoogleProvider,
        compute_network: typing.Optional[cdktf_cdktf_provider_google.DataGoogleComputeNetwork] = None,
        default_disk_size_gb: typing.Optional[jsii.Number] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[DockerVolumes]] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        gitlab_runner_image: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[cdktf_cdktf_provider_google.ComputeInstanceTemplateServiceAccount] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        node_factory: typing.Optional[constructs.INodeFactory] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param gitlab_token: Gitlab token.
        :param provider: Google Cloud Provider.
        :param compute_network: VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param default_disk_size_gb: Gitlab Runner instance Disk size. Default: - 60 GB.
        :param desired_capacity: Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param ebs_size: Gitlab Runner instance EBS size . Default: - ebsSize=60
        :param gitlab_runner_image: Image URL of Gitlab Runner. Default: public.ecr.aws/gitlab/gitlab-runner:alpine
        :param gitlab_url: Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param machine_type: Runner default EC2 instance type. Default: -
        :param max_capacity: Maximum capacity limit for autoscaling group. Default: - desiredCapacity
        :param min_capacity: Minimum capacity limit for autoscaling group. Default: - minCapacity: 1
        :param network_tags: Firewall rules for the Gitlab Runner.
        :param service_account: 
        :param tags: tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']
        :param node_factory: A factory for attaching ``Node``s to the construct. Default: - the default ``Node`` is associated
        '''
        props = GitlabRunnerAutoscalingProps(
            gitlab_token=gitlab_token,
            provider=provider,
            compute_network=compute_network,
            default_disk_size_gb=default_disk_size_gb,
            desired_capacity=desired_capacity,
            docker_volumes=docker_volumes,
            ebs_size=ebs_size,
            gitlab_runner_image=gitlab_runner_image,
            gitlab_url=gitlab_url,
            machine_type=machine_type,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            network_tags=network_tags,
            service_account=service_account,
            tags=tags,
            node_factory=node_factory,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createMetadataStartupScript")
    def create_metadata_startup_script(
        self,
        *,
        gitlab_token: builtins.str,
        provider: cdktf_cdktf_provider_google.GoogleProvider,
        compute_network: typing.Optional[cdktf_cdktf_provider_google.DataGoogleComputeNetwork] = None,
        default_disk_size_gb: typing.Optional[jsii.Number] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[DockerVolumes]] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        gitlab_runner_image: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[cdktf_cdktf_provider_google.ComputeInstanceTemplateServiceAccount] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        node_factory: typing.Optional[constructs.INodeFactory] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param gitlab_token: Gitlab token.
        :param provider: Google Cloud Provider.
        :param compute_network: VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param default_disk_size_gb: Gitlab Runner instance Disk size. Default: - 60 GB.
        :param desired_capacity: Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param ebs_size: Gitlab Runner instance EBS size . Default: - ebsSize=60
        :param gitlab_runner_image: Image URL of Gitlab Runner. Default: public.ecr.aws/gitlab/gitlab-runner:alpine
        :param gitlab_url: Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param machine_type: Runner default EC2 instance type. Default: -
        :param max_capacity: Maximum capacity limit for autoscaling group. Default: - desiredCapacity
        :param min_capacity: Minimum capacity limit for autoscaling group. Default: - minCapacity: 1
        :param network_tags: Firewall rules for the Gitlab Runner.
        :param service_account: 
        :param tags: tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']
        :param node_factory: A factory for attaching ``Node``s to the construct. Default: - the default ``Node`` is associated

        :return: Array.
        '''
        props = GitlabRunnerAutoscalingProps(
            gitlab_token=gitlab_token,
            provider=provider,
            compute_network=compute_network,
            default_disk_size_gb=default_disk_size_gb,
            desired_capacity=desired_capacity,
            docker_volumes=docker_volumes,
            ebs_size=ebs_size,
            gitlab_runner_image=gitlab_runner_image,
            gitlab_url=gitlab_url,
            machine_type=machine_type,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            network_tags=network_tags,
            service_account=service_account,
            tags=tags,
            node_factory=node_factory,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "createMetadataStartupScript", [props]))


@jsii.data_type(
    jsii_type="cdktf-gitlab-runner.GitlabRunnerAutoscalingProps",
    jsii_struct_bases=[constructs.ConstructOptions],
    name_mapping={
        "node_factory": "nodeFactory",
        "gitlab_token": "gitlabToken",
        "provider": "provider",
        "compute_network": "computeNetwork",
        "default_disk_size_gb": "defaultDiskSizeGb",
        "desired_capacity": "desiredCapacity",
        "docker_volumes": "dockerVolumes",
        "ebs_size": "ebsSize",
        "gitlab_runner_image": "gitlabRunnerImage",
        "gitlab_url": "gitlabUrl",
        "machine_type": "machineType",
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "network_tags": "networkTags",
        "service_account": "serviceAccount",
        "tags": "tags",
    },
)
class GitlabRunnerAutoscalingProps(constructs.ConstructOptions):
    def __init__(
        self,
        *,
        node_factory: typing.Optional[constructs.INodeFactory] = None,
        gitlab_token: builtins.str,
        provider: cdktf_cdktf_provider_google.GoogleProvider,
        compute_network: typing.Optional[cdktf_cdktf_provider_google.DataGoogleComputeNetwork] = None,
        default_disk_size_gb: typing.Optional[jsii.Number] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[DockerVolumes]] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        gitlab_runner_image: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[cdktf_cdktf_provider_google.ComputeInstanceTemplateServiceAccount] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param node_factory: A factory for attaching ``Node``s to the construct. Default: - the default ``Node`` is associated
        :param gitlab_token: Gitlab token.
        :param provider: Google Cloud Provider.
        :param compute_network: VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param default_disk_size_gb: Gitlab Runner instance Disk size. Default: - 60 GB.
        :param desired_capacity: Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param ebs_size: Gitlab Runner instance EBS size . Default: - ebsSize=60
        :param gitlab_runner_image: Image URL of Gitlab Runner. Default: public.ecr.aws/gitlab/gitlab-runner:alpine
        :param gitlab_url: Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param machine_type: Runner default EC2 instance type. Default: -
        :param max_capacity: Maximum capacity limit for autoscaling group. Default: - desiredCapacity
        :param min_capacity: Minimum capacity limit for autoscaling group. Default: - minCapacity: 1
        :param network_tags: Firewall rules for the Gitlab Runner.
        :param service_account: 
        :param tags: tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']
        '''
        if isinstance(service_account, dict):
            service_account = cdktf_cdktf_provider_google.ComputeInstanceTemplateServiceAccount(**service_account)
        self._values: typing.Dict[str, typing.Any] = {
            "gitlab_token": gitlab_token,
            "provider": provider,
        }
        if node_factory is not None:
            self._values["node_factory"] = node_factory
        if compute_network is not None:
            self._values["compute_network"] = compute_network
        if default_disk_size_gb is not None:
            self._values["default_disk_size_gb"] = default_disk_size_gb
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if docker_volumes is not None:
            self._values["docker_volumes"] = docker_volumes
        if ebs_size is not None:
            self._values["ebs_size"] = ebs_size
        if gitlab_runner_image is not None:
            self._values["gitlab_runner_image"] = gitlab_runner_image
        if gitlab_url is not None:
            self._values["gitlab_url"] = gitlab_url
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if network_tags is not None:
            self._values["network_tags"] = network_tags
        if service_account is not None:
            self._values["service_account"] = service_account
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def node_factory(self) -> typing.Optional[constructs.INodeFactory]:
        '''A factory for attaching ``Node``s to the construct.

        :default: - the default ``Node`` is associated
        '''
        result = self._values.get("node_factory")
        return typing.cast(typing.Optional[constructs.INodeFactory], result)

    @builtins.property
    def gitlab_token(self) -> builtins.str:
        '''Gitlab token.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN")
        '''
        result = self._values.get("gitlab_token")
        assert result is not None, "Required property 'gitlab_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> cdktf_cdktf_provider_google.GoogleProvider:
        '''Google Cloud Provider.'''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(cdktf_cdktf_provider_google.GoogleProvider, result)

    @builtins.property
    def compute_network(
        self,
    ) -> typing.Optional[cdktf_cdktf_provider_google.DataGoogleComputeNetwork]:
        '''VPC for the Gitlab Runner .

        :default: - A new VPC will be created.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            new_vpc = Vpc(stack, "NewVPC",
                cidr="10.1.0.0/16",
                max_azs=2,
                subnet_configuration=[{
                    "cidr_mask": 26,
                    "name": "RunnerVPC",
                    "subnet_type": SubnetType.PUBLIC
                }],
                nat_gateways=0
            )
            
            GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN", vpc=new_vpc)
        '''
        result = self._values.get("compute_network")
        return typing.cast(typing.Optional[cdktf_cdktf_provider_google.DataGoogleComputeNetwork], result)

    @builtins.property
    def default_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Gitlab Runner instance Disk size.

        :default: - 60 GB.
        '''
        result = self._values.get("default_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        '''Desired capacity limit for autoscaling group.

        :default: - minCapacity, and leave unchanged during deployment

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN", desired_capacity=2)
        '''
        result = self._values.get("desired_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_volumes(self) -> typing.Optional[typing.List[DockerVolumes]]:
        '''add another Gitlab Container Runner Docker Volumes Path at job runner runtime.

        more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section

        :default: - already mount "/var/run/docker.sock:/var/run/docker.sock"

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            dockerVolumes: [
              {
                hostPath: '/tmp/cache',
                containerPath: '/tmp/cache',
              },
            ],
        '''
        result = self._values.get("docker_volumes")
        return typing.cast(typing.Optional[typing.List[DockerVolumes]], result)

    @builtins.property
    def ebs_size(self) -> typing.Optional[jsii.Number]:
        '''Gitlab Runner instance EBS size .

        :default: - ebsSize=60

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            runner = GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN", ebs_size=100)
        '''
        result = self._values.get("ebs_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gitlab_runner_image(self) -> typing.Optional[builtins.str]:
        '''Image URL of Gitlab Runner.

        :default: public.ecr.aws/gitlab/gitlab-runner:alpine

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN", gitlab_runner_image="gitlab/gitlab-runner:alpine")
        '''
        result = self._values.get("gitlab_runner_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gitlab_url(self) -> typing.Optional[builtins.str]:
        '''Gitlab Runner register url .

        :default: - https://gitlab.com/ , The trailing slash is mandatory.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            runner = GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN", gitlab_url="https://gitlab.com/")
        '''
        result = self._values.get("gitlab_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Runner default EC2 instance type.

        :default: -

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN", instance_type="t3.small")
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''Maximum capacity limit for autoscaling group.

        :default: - desiredCapacity

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN", max_capacity=4)
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        '''Minimum capacity limit for autoscaling group.

        :default: - minCapacity: 1

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabRunnerAutoscaling(stack, "runner", gitlab_token="GITLAB_TOKEN", min_capacity=2)
        '''
        result = self._values.get("min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Firewall rules for the Gitlab Runner.'''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_account(
        self,
    ) -> typing.Optional[cdktf_cdktf_provider_google.ComputeInstanceTemplateServiceAccount]:
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[cdktf_cdktf_provider_google.ComputeInstanceTemplateServiceAccount], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''tags for the runner.

        :default: - ['runner', 'gitlab', 'awscdk']
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitlabRunnerAutoscalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DockerVolumes",
    "GitlabRunnerAutoscaling",
    "GitlabRunnerAutoscalingProps",
]

publication.publish()
