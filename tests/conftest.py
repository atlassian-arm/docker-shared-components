import pytest

from fixtures import docker_cli, image


@pytest.fixture(scope='module', params=['0:0', '2001:2001'])
def user(request):
    return request.param