from typing import Any, Dict, List, Optional, Union

import pulumi

from .firewall_rules import FirewallRules, FirewallRulesRuleArgs
from .routes import Routes, RoutesArgs
from .subnets import Subnets, SubnetsSecondaryRangeArgs, SubnetsSubnetArgs
from .vpc import Vpc, VpcRoutingModeEnum


class Network(pulumi.ComponentResource):
    def __init__(
        self,
        resource_name: str,
        project_id: str,
        network_name: str,
        shared_vpc_host: bool = False,
        subnets: List[SubnetsSubnetArgs] = [],
        secondary_ranges: Dict[str, List[SubnetsSecondaryRangeArgs]] = {},
        routing_mode: VpcRoutingModeEnum = VpcRoutingModeEnum.GLOBAL,
        routes: List[Union[Dict[str, Any], RoutesArgs]] = [],
        firewall_rules: List[Union[Dict[str, Any], FirewallRulesRuleArgs]] = [],
        description: Optional[str] = None,
        auto_create_subnetworks: bool = False,
        delete_default_internet_gateway_routes: bool = False,
        mtu: int = 0,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(
            t="zityspace-gcp:network:Network",
            name=resource_name,
            props={},
            opts=opts,
        )

        self.vpc = Vpc(
            "vpc",
            project_id=project_id,
            network_name=network_name,
            shared_vpc_host=shared_vpc_host,
            auto_create_subnetworks=auto_create_subnetworks,
            routing_mode=routing_mode,
            description=description,
            delete_default_internet_gateway_routes=delete_default_internet_gateway_routes,  # noqa
            mtu=mtu,
        )

        self.subnets = Subnets(
            "subnets",
            project_id=project_id,
            network_name=network_name,
            subnets=subnets,  # type: ignore
            secondary_ranges=secondary_ranges,
        )

        self.routes = Routes(
            "route",
            project_id=project_id,
            network_name=network_name,
            routes=routes,
        )

        self.firewall_rules = FirewallRules(
            "firewall_rules",
            project_id=project_id,
            network_name=network_name,
            rules=firewall_rules,
        )
