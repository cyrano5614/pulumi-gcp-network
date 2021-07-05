import sys

sys.path.append("../../src")
from pulumi_gcp_network.vpc import Vpc  # noqa

project_id = "demo-project"
network_name = "example-vpc"

Vpc(
    "demo-vpc",
    project_id=project_id,
    network_name=network_name,
    shared_vpc_host=True,
)
