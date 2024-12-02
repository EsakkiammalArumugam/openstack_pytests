import pytest
import time
import os
from openstack import connection
from openstack.exceptions import ResourceNotFound

@pytest.fixture
def conn():
    """Establish a connection to OpenStack"""
    return connection.Connection(
        auth_url="http://192.168.5.73:5000/v3",
        project_name="admin",
        username="admin",
        password="Esai",
        region_name="RegionOne",
        user_domain_name="Default",
        project_domain_name="Default",
    )

def test_image_creation(conn):
    """Test if the image creation functionality works"""
    image_name = "m1.tiny"
    image_ref = None

    # Assuming you have an image file to upload
    image_file_path = 'cirros-0.4.0-x86_64-disk.img'

    # Create the image
    with open(image_file_path, 'rb') as image_file:
        image = conn.image.create_image(
            name=image_name,
            disk_format='qcow2',  # Choose the correct format based on your image
            container_format='bare',  # Adjust this as needed
            data=image_file
        )

    # Check if the image creation was successful
    assert image is not None
    assert image.name == image_name
    max_retries = 10
    retries = 0
    while retries < max_retries:
        image = conn.image.get_image(image.id)
        if image.status == 'active':
            break
        retries += 1
        time.sleep(5)
    assert image.status == 'active'

    # Optional: Verify the image exists in the OpenStack system
    try:
        found_image = conn.image.get_image(image.id)
        assert found_image is not None
        assert found_image.status == 'active'
    except ResourceNotFound:
        pytest.fail(f"Image {image_name} was not found after creation.")

def test_image_list(conn):
    """Test if the created image is listed"""
    images = list(conn.image.images())
    assert len(images) > 0
    assert any(image.name == 'm1.tiny' for image in images)

