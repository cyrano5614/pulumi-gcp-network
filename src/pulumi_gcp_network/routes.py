from typing import Any, Mapping, Optional, Sequence

import pulumi
import pulumi_gcp as gcp


@pulumi.input_type
class RoutesArgs:
    project_id: pulumi.Input[str] = pulumi.property("projectId")
    network_name: pulumi.Input[str] = pulumi.property("networkName")
    routes: pulumi.Input[Sequence[Mapping[str, pulumi.Input[str]]]] = pulumi.property(
        "routes", default=[]
    )
    module_depends_on: pulumi.Input[Sequence[pulumi.Input[Any]]] = pulumi.property(
        "moduleDependsOn", default=[]
    )


class Routes(pulumi.ComponentResource):
    def __init__(
        self,
        resource_name: str,
        project_id: pulumi.Input[str],
        network_name: pulumi.Input[str],
        routes: pulumi.Input[Sequence[Mapping[str, pulumi.Input[str]]]] = [],
        module_depends_on: pulumi.Input[Sequence[pulumi.Input[Any]]] = [],
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(
            t="zityspace-gcp:network:Routes",
            name=resource_name,
            props={},
            opts=opts,
        )

        self.project_id = project_id
        self.routes = {
            route.get("name", f"{network_name}-route-{i}"): route
            for i, route in enumerate(routes)
        }

        self.created_routes = []
        for i, (name, route) in enumerate(self.routes.items()):

            _created_route = gcp.compute.Route(
                f"route-{i}",
                project=project_id,
                network=network_name,
                name=name,
                description=route.get("description"),
                tags=[tag.strip() for tag in route.get("tags", "").split(",") if tag],
                dest_range=route.get("destination_range"),
                next_hop_gateway="default-internet-gateway"
                if route.get("next_hop_internet", False)
                else None,
                next_hop_ip=route.get("next_hop_ip"),
                next_hop_instance=route.get("next_hop_instance"),
                next_hop_instance_zone=route.get("next_hop_instance_zone"),
                next_hop_vpn_tunnel=route.get("next_hop_vpn_tunnel"),
                next_hop_ilb=route.get("next_hop_ilb"),
                priority=route.get("priority"),
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.created_routes.append(_created_route)
