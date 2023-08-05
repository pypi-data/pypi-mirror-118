# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from ._inputs import *

__all__ = ['ImageArgs', 'Image']

@pulumi.input_type
class ImageArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 registry: pulumi.Input['RegistryArgs'],
                 context: Optional[pulumi.Input[str]] = None,
                 dockerfile: Optional[pulumi.Input[str]] = None,
                 platforms: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Image resource.
        :param pulumi.Input[str] name: The name of the image.
        :param pulumi.Input['RegistryArgs'] registry: The registry to push the image to.
        :param pulumi.Input[str] context: The path to the build context to use.
        :param pulumi.Input[str] dockerfile: The path to the Dockerfile to use.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] platforms: The platforms to build for.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "registry", registry)
        if context is None:
            context = '.'
        if context is not None:
            pulumi.set(__self__, "context", context)
        if dockerfile is None:
            dockerfile = 'Dockerfile'
        if dockerfile is not None:
            pulumi.set(__self__, "dockerfile", dockerfile)
        if platforms is not None:
            pulumi.set(__self__, "platforms", platforms)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the image.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def registry(self) -> pulumi.Input['RegistryArgs']:
        """
        The registry to push the image to.
        """
        return pulumi.get(self, "registry")

    @registry.setter
    def registry(self, value: pulumi.Input['RegistryArgs']):
        pulumi.set(self, "registry", value)

    @property
    @pulumi.getter
    def context(self) -> Optional[pulumi.Input[str]]:
        """
        The path to the build context to use.
        """
        return pulumi.get(self, "context")

    @context.setter
    def context(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "context", value)

    @property
    @pulumi.getter
    def dockerfile(self) -> Optional[pulumi.Input[str]]:
        """
        The path to the Dockerfile to use.
        """
        return pulumi.get(self, "dockerfile")

    @dockerfile.setter
    def dockerfile(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dockerfile", value)

    @property
    @pulumi.getter
    def platforms(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The platforms to build for.
        """
        return pulumi.get(self, "platforms")

    @platforms.setter
    def platforms(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "platforms", value)


class Image(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 context: Optional[pulumi.Input[str]] = None,
                 dockerfile: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platforms: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 registry: Optional[pulumi.Input[pulumi.InputType['RegistryArgs']]] = None,
                 __props__=None):
        """
        Builds a Docker image using Buildkit and pushes it to a registry.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] context: The path to the build context to use.
        :param pulumi.Input[str] dockerfile: The path to the Dockerfile to use.
        :param pulumi.Input[str] name: The name of the image.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] platforms: The platforms to build for.
        :param pulumi.Input[pulumi.InputType['RegistryArgs']] registry: The registry to push the image to.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ImageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Builds a Docker image using Buildkit and pushes it to a registry.

        :param str resource_name: The name of the resource.
        :param ImageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ImageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 context: Optional[pulumi.Input[str]] = None,
                 dockerfile: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platforms: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 registry: Optional[pulumi.Input[pulumi.InputType['RegistryArgs']]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ImageArgs.__new__(ImageArgs)

            if context is None:
                context = '.'
            __props__.__dict__["context"] = context
            if dockerfile is None:
                dockerfile = 'Dockerfile'
            __props__.__dict__["dockerfile"] = dockerfile
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["platforms"] = platforms
            if registry is None and not opts.urn:
                raise TypeError("Missing required property 'registry'")
            __props__.__dict__["registry"] = registry
            __props__.__dict__["context_digest"] = None
            __props__.__dict__["digest"] = None
            __props__.__dict__["image_digest"] = None
            __props__.__dict__["registry_server"] = None
        super(Image, __self__).__init__(
            'docker-buildkit:index:Image',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Image':
        """
        Get an existing Image resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ImageArgs.__new__(ImageArgs)

        __props__.__dict__["context"] = None
        __props__.__dict__["context_digest"] = None
        __props__.__dict__["digest"] = None
        __props__.__dict__["dockerfile"] = None
        __props__.__dict__["image_digest"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["platforms"] = None
        __props__.__dict__["registry_server"] = None
        return Image(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def context(self) -> pulumi.Output[str]:
        """
        The path to the build context to use.
        """
        return pulumi.get(self, "context")

    @property
    @pulumi.getter(name="contextDigest")
    def context_digest(self) -> pulumi.Output[str]:
        """
        The digest of the build context.
        """
        return pulumi.get(self, "context_digest")

    @property
    @pulumi.getter
    def digest(self) -> pulumi.Output[Optional[str]]:
        """
        The bare digest of the image manifest without the docker registry prefix
        """
        return pulumi.get(self, "digest")

    @property
    @pulumi.getter
    def dockerfile(self) -> pulumi.Output[str]:
        """
        The path to the Dockerfile to use.
        """
        return pulumi.get(self, "dockerfile")

    @property
    @pulumi.getter(name="imageDigest")
    def image_digest(self) -> pulumi.Output[str]:
        """
        The fully-qualified digest of the image manifest.
        """
        return pulumi.get(self, "image_digest")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the image.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platforms(self) -> pulumi.Output[Sequence[str]]:
        """
        The platforms to build for.
        """
        return pulumi.get(self, "platforms")

    @property
    @pulumi.getter(name="registryServer")
    def registry_server(self) -> pulumi.Output[str]:
        """
        The URL of the registry server hosting the image.
        """
        return pulumi.get(self, "registry_server")

