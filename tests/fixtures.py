import pytest

import os

import docker
import requests


MAC_PRODUCT_KEY = os.environ.get('MAC_PRODUCT_KEY') or 'docker-testapp'
DOCKER_VERSION_ARG = os.environ.get('DOCKER_VERSION_ARG')
DOCKERFILES = (os.environ.get('DOCKERFILES') or 'Dockerfile').split(',')


# This fixture returns a temporary Docker CLI that cleans up running test containers after each test
@pytest.fixture
def docker_cli():
    docker_cli = docker.from_env()
    yield docker_cli
    for container in docker_cli.containers.list():
        for tag in container.image.tags:
            if tag.startswith(MAC_PRODUCT_KEY):
                container.remove(force=True)


# This fixture returns a built image for each Dockerfile
@pytest.fixture(scope='module', params=DOCKERFILES)
def image(request):
    buildargs = {}
    if MAC_PRODUCT_KEY != 'docker-testapp':
        r = requests.get(f'https://marketplace.atlassian.com/rest/2/products/key/{MAC_PRODUCT_KEY}/versions/latest')
        version = r.json().get('name')
        buildargs[DOCKER_VERSION_ARG] = version
    docker_cli = docker.from_env()
    tag = ''.join(ch for ch in request.param.lower() if ch.isalnum())
    image = docker_cli.images.build(path='.',
                                    tag=f'{MAC_PRODUCT_KEY}:{tag}',
                                    buildargs=buildargs,
                                    dockerfile=request.param,
                                    rm=True)[0]
    return image