from typing import Mapping, Optional, Sequence

import pulumi

# import pulumi_gcp as gcp


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
        subnets: pulumi.Input[Sequence[Mapping[str, pulumi.Input[str]]]],
        secondary_ranges: pulumi.Input[
            Mapping[
                pulumi.Input[str],
                Sequence[Mapping[pulumi.Input[str], pulumi.Input[str]]],
            ]
        ] = {},
        opts: Optional[pulumi.ResourceOptions] = None,
    ):

        super().__init__(
            t="zityspace-gcp:network:Subnets",
            name=resource_name,
            props={},
            opts=opts,
        )
