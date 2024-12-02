import pytest
import openstack

# Setup function to authenticate with OpenStack
@pytest.fixture(scope="module")
def connection():
    conn = openstack.connection.Connection(
        auth_url="http://192.168.5.73:5000/v3",
        project_name="admin",
        username="admin",
        password="Esai",
        region_name="RegionOne",
        user_domain_name="Default",
        project_domain_name="Default",
    )
    yield conn
    conn.close()

# Test for creating a flavor
def test_create_flavor(connection):
    flavor_name = "test-flavor"
    ram = 2048  # RAM in MB
    vcpus = 2    # Number of virtual CPUs
    disk = 20    # Disk space in GB
    
    # Create a new flavor
    flavor = connection.compute.create_flavor(
        name=flavor_name, ram=ram, vcpus=vcpus, disk=disk
    )

    assert flavor is not None, "Flavor creation failed"
    assert flavor.name == flavor_name, f"Expected flavor name '{flavor_name}', but got '{flavor.name}'"
    assert flavor.ram == ram, f"Expected RAM '{ram}MB', but got '{flavor.ram}MB'"
    assert flavor.vcpus == vcpus, f"Expected VCPUs '{vcpus}', but got '{flavor.vcpus}'"
    assert flavor.disk == disk, f"Expected Disk space '{disk}GB', but got '{flavor.disk}GB'"

    # Cleanup: Delete the created flavor
    #connection.compute.delete_flavor(flavor)


