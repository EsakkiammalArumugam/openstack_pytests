import pytest
from openstack import connection

@pytest.fixture
def os_connection():
    """Fixture to establish connection to OpenStack."""
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

def test_create_security_group(os_connection):
    """Test security group creation."""
    # Define the security group name and description
    security_group_name = "test-security-group"
    security_group_description = "A test security group"

    # Create a security group
    sec_group = os_connection.network.create_security_group(
        name=security_group_name,
        description=security_group_description
    )

    # Assert the security group creation
    assert sec_group is not None, "Security group creation failed"
    assert sec_group.name == security_group_name, f"Expected name {security_group_name}, but got {sec_group.name}"
    assert sec_group.description == security_group_description, f"Expected description {security_group_description}, but got {sec_group.description}"

def test_list_security_groups(os_connection):
    """Test listing security groups."""
    security_groups = list(os_connection.network.security_groups())

    # Assert the security group is in the list
    assert any(
        sg.name == "test-security-group" for sg in security_groups
    ), "Security group not found in the list"

def test_security_group_rules(os_connection):
    """Test adding rules to the security group."""
    # Find the security group
    sec_group = next(
        (sg for sg in os_connection.network.security_groups() if sg.name == "test-security-group"),
        None
    )

    assert sec_group is not None, "Security group not found"

    # Create a rule (example: allowing TCP on port 22)
    rule = os_connection.network.create_security_group_rule(
        security_group_id=sec_group.id,
        direction="ingress",
        protocol="tcp",
        port_range_min=22,
        port_range_max=22,
        remote_ip_prefix="0.0.0.0/0"
    )

    # Verify the rule was added
    assert rule is not None, "Security group rule creation failed"
    assert rule.protocol == "tcp", f"Expected protocol tcp, but got {rule.protocol}"
    assert rule.port_range_min == 22, f"Expected port 22, but got {rule.port_range_min}"


