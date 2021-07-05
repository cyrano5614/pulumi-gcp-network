import sys

sys.path.append("../../src")
from pulumi_gcp_network.network import Network  # noqa

project_id = "demo-project"
network_name = "example-vpc"

subnets = [
    {
        "subnet_name": "subnet-01",
        "subnet_ip": "10.10.10.0/24",
        "subnet_region": "us-west1",
    },
    {
        "subnet_name": "subnet-02",
        "subnet_ip": "10.10.20.0/24",
        "subnet_region": "us-west1",
        "subnet_private_access": True,
        "subnet_flow_logs": True,
        "description": "This subnet has a description",
    },
    {
        "subnet_name": "subnet-03",
        "subnet_ip": "10.10.30.0/24",
        "subnet_region": "us-west1",
        "subnet_flow_logs": True,
        "subnet_flow_logs_interval": "INTERVAL_10_MIN",
        "subnet_flow_logs_sampling": 0.7,
        "subnet_flow_logs_metadata": "INCLUDE_ALL_METADATA",
    },
]

secondary_ranges = {
    "subnet-01": [
        {
            "range_name": "subnet-01-secondary-01",
            "ip_cidr_range": "192.168.64.0/24",
        },
    ],
    "subnet-02": [],
}

demo_rules = [
    {
        "name": "test-rule-1",
        "description": "Test rule 1",
        "ranges": ["0.0.0.0/0"],
        "allow": [
            {
                "protocol": "tcp",
                "ports": ["22"],
            }
        ],
        "deny": [],
        "log_config": None,
    },
]

Network(
    "network",
    project_id=project_id,
    network_name=network_name,
    subnets=subnets,
    secondary_ranges=secondary_ranges,
    firewall_rules=demo_rules,
)
