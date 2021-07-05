import dataclasses
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import pulumi
import pulumi_gcp as gcp
from pydantic import BaseModel

if TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


@static_check_init_args
class SubnetPurposeArgsEnum(str, Enum):
    private = "PRIVATE"
    internal_https_load_balancer = "INTERNAL_HTTPS_LOAD_BALANCER"


@static_check_init_args
class SubnetRoleArgsEnum(str, Enum):
    active = "ACTIVE"
    backup = "BACKUP"


@static_check_init_args
class SubnetLogsIntervalEnum(str, Enum):
    INTERVAL_5_SEC = "INTERVAL_5_SEC"
    INTERVAL_30_SEC = "INTERVAL_30_SEC"
    INTERVAL_1_MIN = "INTERVAL_1_MIN"
    INTERVAL_5_MIN = "INTERVAL_5_MIN"
    INTERVAL_10_MIN = "INTERVAL_10_MIN"
    INTERVAL_15_MIN = "INTERVAL_15_MIN"


@static_check_init_args
class SubnetsSubnetArgs(BaseModel):
    # required
    subnet_name: str
    subnet_ip: str
    subnet_region: str

    # optional
    subnet_description: Optional[str] = None
    subnet_private_access: bool = False
    subnet_flow_logs: bool = False
    subnet_flow_logs_interval: SubnetLogsIntervalEnum = (
        SubnetLogsIntervalEnum.INTERVAL_5_SEC
    )
    subnet_flow_logs_sampling: float = 0.5
    subnet_flow_logs_metadata: str = "INCLUDE_ALL_METADATA"


@static_check_init_args
class SubnetsSecondaryRangeArgs(BaseModel):
    range_name: str
    ip_cidr_range: str


class Subnets(pulumi.ComponentResource):
    def __init__(
        self,
        resource_name: str,
        project_id: str,
        network_name: str,
        subnets: List[Union[Dict[str, Any], SubnetsSubnetArgs]] = [],
        secondary_ranges: Dict[str, List[SubnetsSecondaryRangeArgs]] = {},
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

        self.created_subnetworks = []
        for i, subnet in enumerate(subnets):

            if not isinstance(subnet, SubnetsSubnetArgs):
                subnet = SubnetsSubnetArgs(**subnet)

            _subnetwork = gcp.compute.Subnetwork(  # type: ignore
                f"subnetwork-{i}",
                name=subnet.subnet_name,
                ip_cidr_range=subnet.subnet_ip,
                region=subnet.subnet_region,
                private_ip_google_access=subnet.subnet_private_access,
                network=network_name,
                project=project_id,
                description=subnet.subnet_description,
                log_config=gcp.compute.SubnetworkLogConfigArgs(  # type: ignore
                    aggregation_interval=subnet.subnet_flow_logs_interval,
                    flow_sampling=subnet.subnet_flow_logs_sampling,
                    metadata=subnet.subnet_flow_logs_metadata,
                )
                if subnet.subnet_flow_logs
                else {},
                secondary_ip_ranges=[]
                if not secondary_ranges.get(subnet.subnet_name)
                else [
                    self.get_secondary_ip_range(_secondary_range)
                    for _secondary_range in secondary_ranges[subnet.subnet_name]
                ],
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.created_subnetworks.append(_subnetwork)

    @staticmethod
    def get_secondary_ip_range(
        secondary_range: Union[Dict[str, str], SubnetsSecondaryRangeArgs],
    ) -> gcp.compute.SubnetworkSecondaryIpRangeArgs:  # type: ignore

        if not isinstance(secondary_range, SubnetsSecondaryRangeArgs):
            secondary_range = SubnetsSecondaryRangeArgs(**secondary_range)

        return gcp.compute.SubnetworkSecondaryIpRangeArgs(  # type: ignore
            range_name=secondary_range.range_name,
            ip_cidr_range=secondary_range.ip_cidr_range,
        )
