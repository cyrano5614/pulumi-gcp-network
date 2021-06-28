import unittest

import pulumi


class TestMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + "_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


pulumi.runtime.set_mocks(TestMocks())

# It's important to import _after_ the mocks are defined.
from pulumi_gcp_network.routes import (  # noqa isort:skip type: ignore
    Routes,
)

TEST_NAME = "test-routes"
TEST_PROJECT_ID = "test"
TEST_NETWORK_NAME = "test-network"
TEST_ROUTES = [
    {
        "name": "test-egress-inet",
        "description": "route through IGW to access internet",
        "destination_range": "0.0.0.0/0",
        "tags": "egress-inet",
        "next_hop_internet": "true",
    },
    {
        "description": "route through ilb",
        "destination_range": "10.10.20.0/24",
        "tags": "foo, bar, ham",
    },
]


class TestingRoutes(unittest.TestCase):
    @pulumi.runtime.test
    def setUp(self):
        self.routes = Routes(
            TEST_NAME,
            project_id=TEST_PROJECT_ID,
            network_name=TEST_NETWORK_NAME,
            routes=TEST_ROUTES,
        )

    @pulumi.runtime.test
    def test_project_id(self):
        def check_project_id(args):
            project_id = args[0]
            self.assertEqual(project_id, TEST_PROJECT_ID)

        return pulumi.Output.all(self.routes.project_id).apply(check_project_id)

    @pulumi.runtime.test
    def test_urn(self):
        def check_urn(args):
            urn = args[0][0]
            self.assertIn(TEST_NAME, urn)

        return pulumi.Output.all([self.routes.urn]).apply(check_urn)

    @pulumi.runtime.test
    def test_created_routes_length(self):
        def check_created_routes_length(args):
            created_routes = args
            self.assertEqual(len(created_routes), len(TEST_ROUTES))

        return pulumi.Output.all(*self.routes.created_routes).apply(
            check_created_routes_length
        )

    @pulumi.runtime.test
    def test_created_routes_tags(self):
        def check_created_routes_tags(args):
            first_tags, second_tags = args
            self.assertEqual(["egress-inet"], first_tags)
            self.assertEqual(["foo", "bar", "ham"], second_tags)

        return pulumi.Output.all(
            *[route.tags for route in self.routes.created_routes]
        ).apply(check_created_routes_tags)

    @pulumi.runtime.test
    def test_created_routes_next_hop_gateway(self):
        def check_created_routes_next_hop_gateway(args):
            first_gateway, second_gateway = args

            self.assertEqual("default-internet-gateway", first_gateway)
            self.assertIsNone(second_gateway)

        return pulumi.Output.all(
            *[route.next_hop_gateway for route in self.routes.created_routes]
        ).apply(check_created_routes_next_hop_gateway)

    @pulumi.runtime.test
    def test_created_routes_name(self):
        def check_created_routes_name(args):
            first_gateway, second_gateway = args

            self.assertEqual("test-egress-inet", first_gateway)
            self.assertEqual("test-network-route-1", second_gateway)

        return pulumi.Output.all(
            *[route.name for route in self.routes.created_routes]
        ).apply(check_created_routes_name)
