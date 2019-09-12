import pytest

from helpers import run_image, wait_for_proc

# Helper functions to get config values from support scripts
def get_app_home(container):
    cmd = "/bin/bash -c 'source /opt/atlassian/support/common.sh && echo ${APP_HOME}'"
    home = container.run(cmd).stdout.strip()
    return home

def get_bootstrap_proc(container):
    cmd = "/bin/bash -c 'source /opt/atlassian/support/common.sh && echo ${BOOTSTRAP_PROC}'"
    proc = container.run(cmd).stdout.strip()
    return proc


def test_thread_dumps(docker_cli, image, user):
    COUNT = 3
    INTERVAL = 1
    container = run_image(docker_cli, image, user=user)
    wait_for_proc(container, get_bootstrap_proc(container))
    
    thread_cmd = f'/opt/atlassian/support/thread-dumps.sh --count {COUNT} --interval {INTERVAL}'
    container.run(thread_cmd)
    
    find_thread_cmd = f'find {get_app_home(container)} -name "*_THREADS.*.txt"'
    thread_dumps = container.run(find_thread_cmd).stdout.splitlines()
    assert len(thread_dumps) == 3
    
    find_top_cmd = f'find {get_app_home(container)} -name "*_CPU_USAGE.*.txt"'
    top_dumps = container.run(find_top_cmd).stdout.splitlines()
    assert len(top_dumps) == 3

def test_thread_dumps_no_top(docker_cli, image, user):
    COUNT = 3
    INTERVAL = 1
    container = run_image(docker_cli, image, user=user)
    wait_for_proc(container, get_bootstrap_proc(container))
    
    thread_cmd = f'/opt/atlassian/support/thread-dumps.sh --no-top --count {COUNT} --interval {INTERVAL}'
    container.run(thread_cmd)
    
    find_thread_cmd = f'find {get_app_home(container)} -name "*_THREADS.*.txt"'
    thread_dumps = container.run(find_thread_cmd).stdout.splitlines()
    assert len(thread_dumps) == 3
    
    find_top_cmd = f'find {get_app_home(container)} -name "*_CPU_USAGE.*.txt"'
    top_dumps = container.run(find_top_cmd).stdout.splitlines()
    assert len(top_dumps) == 0

def test_heap_dump(docker_cli, image, user):
    container = run_image(docker_cli, image, user=user)
    wait_for_proc(container, get_bootstrap_proc(container))
    
    heap_cmd = f'/opt/atlassian/support/heap-dump.sh'
    container.run(heap_cmd)
    
    ls_cmd = f'ls -la {get_app_home(container)}/heap.bin'
    heap_dump = container.run(ls_cmd).stdout.splitlines()
    assert len(heap_dump) == 1

def test_heap_dump_overwrite_false(docker_cli, image, user):
    container = run_image(docker_cli, image, user=user)
    wait_for_proc(container, get_bootstrap_proc(container))
    
    heap_cmd = f'/opt/atlassian/support/heap-dump.sh'
    ls_cmd = f'ls -la --time-style=full-iso {get_app_home(container)}/heap.bin'
    
    container.run(heap_cmd)
    heap_dump_1 = container.run(ls_cmd).stdout.splitlines()
    container.run(heap_cmd)
    heap_dump_2 = container.run(ls_cmd).stdout.splitlines()
    assert heap_dump_1 == heap_dump_2

def test_heap_dump_overwrite_true(docker_cli, image, user):
    container = run_image(docker_cli, image, user=user)
    wait_for_proc(container, get_bootstrap_proc(container))
    
    heap_cmd = f'/opt/atlassian/support/heap-dump.sh --force'
    ls_cmd = f'ls -la {get_app_home(container)}/heap.bin'
    
    container.run(heap_cmd)
    heap_dump_1 = container.run(ls_cmd).stdout.splitlines()
    container.run(heap_cmd)
    heap_dump_2 = container.run(ls_cmd).stdout.splitlines()
    assert heap_dump_1 != heap_dump_2
    
