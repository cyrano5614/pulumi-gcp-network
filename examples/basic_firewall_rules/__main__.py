import sys

sys.path.append("../../src")
from pulumi_gcp_network.firewall_rules import FirewallRules  # noqa

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
firewall_rules = FirewallRules(
    "demo-firewall",
    project_id="demo-project-id",
    network_name="demo-network-name",
    rules=demo_rules,
)
