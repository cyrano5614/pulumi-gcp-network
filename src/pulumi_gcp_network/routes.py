import dataclasses
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

import pulumi
import pulumi_gcp as gcp
from pydantic import BaseModel, Field

if TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


@static_check_init_args
class RoutesArgs(BaseModel):
    # required
    destination_range: str

    # optional
    tags: Optional[str] = None
    name: Optional[str] = None
    next_hop_internet: bool = False
    next_hop_ip: Optional[str] = None
    description: Optional[str] = None
    next_hop_instance: Optional[str] = None
    next_hop_instance_zone: Optional[str] = None
    next_hop_vpn_tunnel: Optional[str] = None
    next_hop_ilb: Optional[str] = None
    priority: int = Field(default=1000, ge=0, le=65535)


class Routes(pulumi.ComponentResource):
    def __init__(
        self,
        resource_name: str,
        project_id: str,
        network_name: str,
        routes: List[Union[Dict[str, Any], RoutesArgs]] = [],
        module_depends_on: pulumi.Input[Sequence[pulumi.Input[Any]]] = [],
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """__init__.

        :param resource_name: pulumi resource name.
        :type resource_name: str
        :param project_id: The ID of the project where the routes will be created.
        :type project_id: pulumi.Input[str]
        :param network_name: The name of the network where routes will be created.
        :type network_name: pulumi.Input[str]
        :param routes: List of routes being created in this VPC.
        :type routes: pulumi.Input[Sequence[Mapping[str, pulumi.Input[str]]]]
        :param module_depends_on: List of modules or resources this module depends on.
        :type module_depends_on: pulumi.Input[Sequence[pulumi.Input[Any]]]
        :param opts: Options for pulumi resource.
        :type opts: Optional[pulumi.ResourceOptions]
        """
        super().__init__(
            t="zityspace-gcp:network:Routes",
            name=resource_name,
            props={},
            opts=opts,
        )

        self.project_id = project_id

        self.created_routes = []

        for i, route in enumerate(routes):
            if not isinstance(route, RoutesArgs):
                route = RoutesArgs(**route)

            if not route.name:
                route.name = f"route-{network_name}-{i}"

            _created_route = gcp.compute.Route(  # type: ignore
                route.name,
                project=project_id,
                network=network_name,
                name=route.name,
                description=route.description,
                tags=self.get_tags(route.tags),
                dest_range=route.destination_range,
                next_hop_gateway="default-internet-gateway"
                if route.next_hop_internet
                else None,
                next_hop_ip=route.next_hop_ip,
                next_hop_instance=route.next_hop_instance,
                next_hop_instance_zone=route.next_hop_instance_zone,
                next_hop_vpn_tunnel=route.next_hop_vpn_tunnel,
                next_hop_ilb=route.next_hop_ilb,
                priority=route.priority,
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.created_routes.append(_created_route)

    @staticmethod
    def get_tags(tags: Optional[str] = None) -> List[str]:

        if tags is None:
            tags = ""

        return [tag.strip() for tag in tags.split(",") if tag]
