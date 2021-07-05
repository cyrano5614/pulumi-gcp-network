import unittest

import pulumi


class TestMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + "_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


pulumi.runtime.set_mocks(TestMocks())

# It's important to import _after_ the mocks are defined.
from pulumi_gcp_network.vpc import (  # noqa isort:skip type: ignore
    Vpc,
)

TEST_NAME = "test-vpc"
TEST_PROJECT_ID = "test"
TEST_NETWORK_NAME = "test-vpc"
TEST_SUBNETS = [
    {
        "subnet_name": "test-subnet-1",
        "subnet_ip": "10.10.10.0/24",
        "subnet_region": "us-west1",
    },
    {
        "subnet_name": "test-subnet-2",
        "subnet_ip": "10.10.20.0/24",
        "subnet_region": "us-west1",
        "subnet_private_access": True,
        "subnet_flow_logs": True,
    },
    {
        "subnet_name": "test-subnet-3",
        "subnet_ip": "10.10.30.0/24",
        "subnet_region": "us-west1",
        "subnet_flow_logs": True,
        "subnet_flow_logs_interval": "INTERVAL_15_MIN",
        "subnet_flow_logs_sampling": 0.9,
        "subnet_flow_logs_metadata": "INCLUDE_ALL_METADATA",
    },
    {
        "subnet_name": "test-subnet-4",
        "subnet_ip": "10.10.40.0/24",
        "subnet_region": "us-west1",
    },
]

TEST_SECONDARY_RANGES = {
    "test-subnet-1": [
        {
            "range_name": "test-subnet-1-01",
            "ip_cidr_range": "192.168.64.0/24",
        },
        {
            "range_name": "test-subnet-1-02",
            "ip_cidr_range": "192.168.65.0/24",
        },
    ],
    "test-subnet-2": [],
    "test-subnet-3": [
        {
            "range_name": "test-subnet-3-01",
            "ip_cidr_range": "192.168.66.0/24",
        },
    ],
}


class TestingVpc(unittest.TestCase):
    @pulumi.runtime.test
    def setUp(self):
        self.vpc = Vpc(
            TEST_NAME,
            project_id=TEST_PROJECT_ID,
            network_name=TEST_NETWORK_NAME,
        )

    @pulumi.runtime.test
    def test_project_id(self):
        def check_project_id(args):
            project_id = args[0]
            self.assertEqual(project_id, TEST_PROJECT_ID)

        return pulumi.Output.all(self.vpc.project_id).apply(check_project_id)

    @pulumi.runtime.test
    def test_urn(self):
        def check_urn(args):
            urn = args[0][0]
            self.assertIn(TEST_NAME, urn)

        return pulumi.Output.all([self.vpc.urn]).apply(check_urn)
