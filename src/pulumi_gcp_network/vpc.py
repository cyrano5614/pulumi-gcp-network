import dataclasses
from enum import Enum
from typing import TYPE_CHECKING, Optional

import pulumi
import pulumi_gcp as gcp

if TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


@static_check_init_args
class VpcRoutingModeEnum(str, Enum):
    GLOBAL = "GLOBAL"
    REGIONAL = "REGIONAL"


class Vpc(pulumi.ComponentResource):
    def __init__(
        self,
        resource_name: str,
        project_id: str,
        network_name: str,
        routing_mode: VpcRoutingModeEnum = VpcRoutingModeEnum.GLOBAL,
        shared_vpc_host: bool = False,
        description: Optional[str] = None,
        auto_create_subnetworks: bool = False,
        delete_default_internet_gateway_routes: bool = False,
        mtu: int = 0,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(
            t="zityspace-gcp:network:Vpc",
            name=resource_name,
            props={},
            opts=opts,
        )

        self.project_id = project_id

        self.vpc = gcp.compute.Network(  # type: ignore
            "vpc",
            name=network_name,
            auto_create_subnetworks=auto_create_subnetworks,
            routing_mode=routing_mode,
            project=project_id,
            description=description,
            delete_default_routes_on_create=delete_default_internet_gateway_routes,
            mtu=mtu,
        )

        self.shared_vpc_host = None
        if shared_vpc_host:
            self.shared_vpc_host = gcp.compute.SharedVPCHostProject(  # type: ignore
                "shared_vpc_host",
                project=project_id,
            )
