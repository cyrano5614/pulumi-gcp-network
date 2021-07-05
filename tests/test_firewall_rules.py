import unittest

import pulumi


class TestMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + "_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


pulumi.runtime.set_mocks(TestMocks())

# It's important to import _after_ the mocks are defined.
from pulumi_gcp_network.firewall_rules import (  # noqa isort:skip type: ignore
    FirewallRules,
)

TEST_NAME = "test-firewall-rules"
TEST_PROJECT_ID = "test"
TEST_NETWORK_NAME = "test-network"
TEST_FIREWALLRULES = [
    {
        "name": "test-rule-1",
        "description": "Test rule 1",
        "ranges": ["0.0.0.0/0"],
        "allows": [
            {
                "protocol": "tcp",
                "ports": ["22"],
            }
        ],
        "denies": [],
        "log_config": None,
    },
    {
        "name": "test-rule-2",
        "description": "Test rule 2",
        "ranges": ["10.10.20.0/24"],
        "direction": "EGRESS",
    },
]


class TestingFirewallRules(unittest.TestCase):
    @pulumi.runtime.test
    def setUp(self):
        self.firewall_rules = FirewallRules(
            TEST_NAME,
            project_id=TEST_PROJECT_ID,
            network_name=TEST_NETWORK_NAME,
            rules=TEST_FIREWALLRULES,
        )

    @pulumi.runtime.test
    def test_project_id(self):
        def check_project_id(args):
            project_id = args[0]
            self.assertEqual(project_id, TEST_PROJECT_ID)

        return pulumi.Output.all(self.firewall_rules.project_id).apply(check_project_id)

    @pulumi.runtime.test
    def test_urn(self):
        def check_urn(args):
            urn = args[0][0]
            self.assertIn(TEST_NAME, urn)

        return pulumi.Output.all([self.firewall_rules.urn]).apply(check_urn)

    @pulumi.runtime.test
    def test_created_firewall_rules_length(self):
        def check_created_firewall_rules_length(args):
            created_firewall_rules = args
            self.assertEqual(len(created_firewall_rules), len(TEST_FIREWALLRULES))

        return pulumi.Output.all(*self.firewall_rules.created_firewall_rules).apply(
            check_created_firewall_rules_length
        )

    @pulumi.runtime.test
    def test_created_firewall_ranges(self):
        def check_created_firewall_source_ranges(args):
            ranges = args

            self.assertEqual([["0.0.0.0/0"], None], ranges)

        def check_created_firewall_destination_ranges(args):
            ranges = args

            self.assertEqual([None, ["10.10.20.0/24"]], ranges)

        pulumi.Output.all(
            *[
                route.source_ranges
                for route in self.firewall_rules.created_firewall_rules
            ]
        ).apply(check_created_firewall_source_ranges)

        pulumi.Output.all(
            *[
                route.destination_ranges
                for route in self.firewall_rules.created_firewall_rules
            ]
        ).apply(check_created_firewall_destination_ranges)
