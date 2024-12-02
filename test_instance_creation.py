import pytest
from openstack import connection
import logging

# Configuration for OpenStack connection
@pytest.fixture(scope="module")
def openstack_connection():
    # Replace with your actual OpenStack connection details
    conn = connection.Connection(
        auth_url="http://192.168.5.73:5000/v3",
        project_name="admin",
        username="admin",
        password="Esai",
        region_name="RegionOne",
        user_domain_name="Default",
        project_domain_name="Default",
    )
    return conn

# Helper function to find resources or fail
def find_resource_or_fail(conn, resource_type, name):
    try:
        # Use appropriate methods to find the resource by name
        resource = None
        if resource_type == "flavor":
            resource = conn.compute.find_flavor(name)
        elif resource_type == "image":
            resource = conn.image.find_image(name)
        elif resource_type == "network":
            resource = conn.network.find_network(name)
        
        if resource is None:
            raise ResourceNotFound(f"{resource_type.capitalize()} with name '{name}' not found.")
        
        return resource
    except Exception as e:
        logging.error(f"Error finding {resource_type} {name}: {str(e)}")
        raise

# Test case for creating a Cirros instance using a specific flavor, image, and network
@pytest.mark.usefixtures("openstack_connection")
def test_create_cirros_instance(openstack_connection):
    flavor_name = "test-flavor"  # Ensure this flavor exists in your OpenStack
    image_name = "m1.tiny"  # Make sure this image exists in your OpenStack
    network_name = "selfservice"  # Ensure this network exists in your OpenStack

    try:
        # Find flavor, image, and network using the helper function
        flavor = find_resource_or_fail(openstack_connection, "flavor", flavor_name)
        image = find_resource_or_fail(openstack_connection, "image", image_name)
        network = find_resource_or_fail(openstack_connection, "network", network_name)

        # Create the server instance
        server = openstack_connection.compute.create_server(
            name="test-cirros-instance",
            image_id=image.id,
            flavor_id=flavor.id,
            networks=[{"uuid": network.id}],
        )

        # Wait for the instance to become active
        openstack_connection.compute.wait_for_server(server)

        # Get the server details and assert it is active
        server = openstack_connection.compute.get_server(server.id)
        assert server.status == "ACTIVE", (
            f"Server {server.name} is not active, status: {server.status}"
        )
        print(f"Server {server.name} created successfully and is active.")
        
    except Exception as e:
        logging.error(f"Error creating Cirros instance: {str(e)}")
        pytest.fail(f"Test failed: {str(e)}")

