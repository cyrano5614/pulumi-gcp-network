import dataclasses
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import pulumi
import pulumi_gcp as gcp
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


@static_check_init_args
class FirewallDirectionEnum(str, Enum):
    INGRESS = "INGRESS"
    EGRESS = "EGRESS"


@static_check_init_args
class FirewallLogConfigMetadataEnum(str, Enum):
    EXCLUDE_ALL_METADATA = "EXCLUDE_ALL_METADATA"
    INCLUDE_ALL_METADATA = "INCLUDE_ALL_METADATA"


@static_check_init_args
class FirewallRulesAllowDenyArgs(BaseModel):
    protocol: str
    ports: Union[Union[str, int], List[Union[str, int]]]


@static_check_init_args
class FirewallRulesLogConfigArgs(BaseModel):
    metadata: FirewallLogConfigMetadataEnum = (
        FirewallLogConfigMetadataEnum.INCLUDE_ALL_METADATA
    )


@static_check_init_args
class FirewallRulesRuleArgs(BaseModel):
    name: str
    description: Optional[str] = None
    direction: FirewallDirectionEnum = FirewallDirectionEnum.INGRESS
    priority: int = Field(default=1000, ge=0, le=65535)
    ranges: List[str] = []
    source_tags: Optional[List[str]] = None
    source_service_accounts: Optional[List[str]] = None
    target_tags: Optional[List[str]] = None
    target_service_accounts: Optional[List[str]] = None
    allow: Optional[List[FirewallRulesAllowDenyArgs]] = None
    deny: Optional[List[FirewallRulesAllowDenyArgs]] = None
    log_config: Optional[FirewallRulesLogConfigArgs] = None


class FirewallRules(pulumi.ComponentResource):
    def __init__(
        self,
        resource_name: str,
        project_id: str,
        network_name: str,
        rules: List[Union[Dict[str, Any], FirewallRulesRuleArgs]] = [],
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(
            t="zityspace-gcp:network:FirewallRules",
            name=resource_name,
            props={},
            opts=opts,
        )

        self.project_id = project_id

        self.created_firewall_rules = []
        for i, rule in enumerate(rules):

            if not isinstance(rule, FirewallRulesRuleArgs):
                rule = FirewallRulesRuleArgs(**rule)

            _rule = gcp.compute.Firewall(  # type: ignore
                f"rule-{rule.name}-{i}",
                name=rule.name,
                description=rule.description,
                direction=rule.direction,
                network=network_name,
                project=project_id,
                source_ranges=rule.ranges if rule.direction == "INGRESS" else None,
                destination_ranges=rule.ranges if rule.direction == "EGRESS" else None,
                source_tags=rule.source_tags,
                source_service_accounts=rule.source_service_accounts,
                target_tags=rule.target_tags,
                target_service_accounts=rule.target_service_accounts,
                priority=rule.priority,
                log_config=rule.log_config,
                denies=[rule.dict() for rule in rule.deny] if rule.deny else None,
                allows=[rule.dict() for rule in rule.allow] if rule.allow else None,
            )
            self.created_firewall_rules.append(_rule)
