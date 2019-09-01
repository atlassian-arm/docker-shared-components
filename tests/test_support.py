import pytest

from helpers import run_image, wait_for_proc

def test_thread_dumps(docker_cli, image):
    COUNT = 3
    INTERVAL = 1
    container = run_image(docker_cli, image)
    wait_for_proc(container, 'org.apache.catalina.startup.Bootstrap')
    
    thread_cmd = f'/opt/atlassian/support/thread-dumps.sh --count {COUNT} --interval {INTERVAL}'
    container.run(thread_cmd)
    
    find_thread_cmd = 'find $JIRA_HOME -wholename "*thread_dumps_*/*_THREADS*"'
    thread_dumps = container.run(find_thread_cmd).stdout.splitlines()
    assert len(thread_dumps) == 3
    
    find_top_cmd = 'find $JIRA_HOME -wholename "*thread_dumps_*/*CPU_USAGE*"'
    top_dumps = container.run(find_top_cmd).stdout.splitlines()
    assert len(top_dumps) == 3

def test_thread_dumps_no_top(docker_cli, image):
    COUNT = 3
    INTERVAL = 1
    container = run_image(docker_cli, image)
    wait_for_proc(container, 'org.apache.catalina.startup.Bootstrap')
    
    thread_cmd = f'/opt/atlassian/support/thread-dumps.sh --no-top --count {COUNT} --interval {INTERVAL}'
    container.run(thread_cmd)
    
    find_thread_cmd = 'find $JIRA_HOME -wholename "*thread_dumps_*/*_THREADS*"'
    thread_dumps = container.run(find_thread_cmd).stdout.splitlines()
    assert len(thread_dumps) == 3
    
    find_top_cmd = 'find $JIRA_HOME -wholename "*thread_dumps_*/*CPU_USAGE*"'
    top_dumps = container.run(find_top_cmd).stdout.splitlines()
    assert len(top_dumps) == 0

def test_heap_dump(docker_cli, image):
    container = run_image(docker_cli, image)
    wait_for_proc(container, 'org.apache.catalina.startup.Bootstrap')
    
    heap_cmd = f'/opt/atlassian/support/heap-dump.sh'
    container.run(heap_cmd)
    
    ls_cmd = 'ls -la $JIRA_HOME/heap.bin'
    heap_dump = container.run(ls_cmd).stdout.splitlines()
    assert len(heap_dump) == 1

def test_heap_dump_overwrite_false(docker_cli, image):
    container = run_image(docker_cli, image)
    wait_for_proc(container, 'org.apache.catalina.startup.Bootstrap')
    
    heap_cmd = f'/opt/atlassian/support/heap-dump.sh'
    ls_cmd = 'ls -la --time-style=full-iso $JIRA_HOME/heap.bin'
    
    container.run(heap_cmd)
    heap_dump_1 = container.run(ls_cmd).stdout.splitlines()
    container.run(heap_cmd)
    heap_dump_2 = container.run(ls_cmd).stdout.splitlines()
    assert heap_dump_1 == heap_dump_2

def test_heap_dump_overwrite_true(docker_cli, image):
    container = run_image(docker_cli, image)
    wait_for_proc(container, 'org.apache.catalina.startup.Bootstrap')
    
    heap_cmd = f'/opt/atlassian/support/heap-dump.sh --force'
    ls_cmd = 'ls -la $JIRA_HOME/heap.bin'
    
    container.run(heap_cmd)
    heap_dump_1 = container.run(ls_cmd).stdout.splitlines()
    container.run(heap_cmd)
    heap_dump_2 = container.run(ls_cmd).stdout.splitlines()
    assert heap_dump_1 != heap_dump_2
    
    