import sys

sys.path.append("../../src")
from pulumi_gcp_network.routes import Routes  # noqa

demo_routes = [
    {
        "name": "egress-internet",
        "description": "route through IGW to access internet",
        "destination_range": "0.0.0.0/0",
        "tags": "egress-inet",
        "next_hop_internet": "true",
    },
    {
        "name": "app-proxy",
        "description": "route through proxy to reach app",
        "destination_range": "10.50.10.0/24",
        "tags": "app-proxy",
        "next_hop_instance": "app-proxy-instance",
        "next_hop_instance_zone": "us-west1-a",
    },
]


firewall_rules = Routes(
    "demo-routes",
    project_id="demo-project-id",
    network_name="demo-network",
    routes=demo_routes,
)
