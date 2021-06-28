from typing import List, Mapping, Optional, Sequence

import pulumi
import pulumi_gcp as gcp


@pulumi.input_type
class SubnetsArgs:
    project_id: pulumi.Input[str] = pulumi.property("projectId")
    network_name: pulumi.Input[str] = pulumi.property("networkName")
    subnets: pulumi.Input[Sequence[Mapping[str, pulumi.Input[str]]]] = pulumi.property(
        "subnets"
    )
    secondary_ranges: pulumi.Input[
        Mapping[
            pulumi.Input[str], Sequence[Mapping[pulumi.Input[str], pulumi.Input[str]]]
        ]
    ] = pulumi.property("secondary_ranges", default={})


class Subnets(pulumi.ComponentResource):
    def __init__(
        self,
        resource_name: str,
        project_id: pulumi.Input[str],
        network_name: pulumi.Input[str],
        subnets: pulumi.Input[Sequence[Mapping[str, pulumi.Input[str]]]],
        secondary_ranges: pulumi.Input[
            Mapping[
                pulumi.Input[str],
                Sequence[Mapping[pulumi.Input[str], pulumi.Input[str]]],
            ]
        ] = {},
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """__init__. # noqa

        :param resource_name: pulumi resource name.
        :type resource_name: str
        :param project_id: The ID of the project where subnets will be created.
        :type project_id: pulumi.Input[str]
        :param network_name: The name of the network where subnets will be created
        :type network_name: pulumi.Input[str]
        :param subnets: The list of subnets being created
        :type subnets: pulumi.Input[Sequence[Mapping[str, pulumi.Input[str]]]]
        :param secondary_ranges: Secondary ranges that will be used in some of the subnets
        :type secondary_ranges: pulumi.Input[
                    Mapping[
                        pulumi.Input[str],
                        Sequence[Mapping[pulumi.Input[str], pulumi.Input[str]]],
                    ]
                ]
        :param opts: Options for pulumi resource.
        :type opts: Optional[pulumi.ResourceOptions]
        """

        super().__init__(
            t="zityspace-gcp:network:Subnets",
            name=resource_name,
            props={},
            opts=opts,
        )

        self.project_id = project_id
        self.subnets = {
            f"{subnet['subnet_region']}/{subnet['subnet_name']}": subnet
            for subnet in subnets
        }

        self.created_subnetworks = []
        for i, (name, subnet) in enumerate(self.subnets.items()):
            _subnetwork = gcp.compute.Subnetwork(
                f"subnetwork-{i}",
                name=subnet["subnet_name"],
                ip_cidr_range=subnet["subnet_ip"],
                region=subnet["subnet_region"],
                private_ip_google_access=subnet.get("subnet_private_access", False),
                network=network_name,
                project=project_id,
                description=subnet.get("description"),
                log_config=gcp.compute.SubnetworkLogConfigArgs(
                    aggregation_interval=subnet.get(
                        "subnet_flow_logs_interval", "INTERVAL_5_SEC"
                    ),
                    flow_sampling=subnet.get("subnet_flow_logs_sampling", 0.5),
                    metadata=subnet.get(
                        "subnet_flow_logs_metadata", "INCLUDE_ALL_METADATA"
                    ),
                )
                if subnet.get("subnet_flow_logs", False)
                else {},
                secondary_ip_ranges=self.get_secondary_ip_ranges(
                    secondary_ranges, subnet["subnet_name"]
                ),
            )
            self.created_subnetworks.append(_subnetwork)

    @staticmethod
    def get_secondary_ip_ranges(
        secondary_ranges: Mapping[str, Sequence[Mapping[str, str]]], subnet_name: str
    ) -> List[gcp.compute.SubnetworkSecondaryIpRangeArgs]:

        _secondary_ranges = secondary_ranges.get(subnet_name, [])

        return [
            gcp.compute.SubnetworkSecondaryIpRangeArgs(
                range_name=_secondary_range["range_name"],
                ip_cidr_range=_secondary_range["ip_cidr_range"],
            )
            for _secondary_range in _secondary_ranges
        ]
