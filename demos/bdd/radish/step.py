# -*- coding: utf-8 -*-

from radish import step, given, when, then
from radish import world

import re
import time

@given("my {name:w} build was flashed")
def build_was_flashed(step, name):
    client   = step.context.client
    settings = step.context.settings
    assert 'builds' in settings
    assert name in settings["builds"]

    image = settings["builds"][name]
    if image != world.build:
        assert target_off(client)
        assert client.sd_write_image(image)
        world.build = image

@when("a kernel version is specified")
def kernel_version_specified(step):
    settings = step.context.settings
    version = None
    if 'kernel' in settings:
        if 'version' in settings["kernel"]:
            version = settings["kernel"]["version"]
    step.context.version = version
    if version is None:
        step.pending()

@then("the running kernel version shall match")
def kernel_version_compliance(step):
    client  = step.context.client
    version = step.context.version
    if version is None:
        step.pending()
    else:
        lines = client.console_run("uname -r").split('\n')
        result = lines[0]
        assert re.match(version, result)

@step("my target is on")
def target_is_on(step):
    client = step.context.client
    settings = step.context.settings

    # Power on the board
    initial_status = client.target_status()
    assert target_on(client)

    # Give target some time to start and check its power status again
    if initial_status != "ON":
        time.sleep(settings["boot"]["delay"])

@step("Linux is running")
def linux_is_running(step):
    client = step.context.client
    step.context.runtime = "???"

    # Check for target console
    online = console_login(client)
    assert online == True

    # Check running system
    client.console_send("cat /proc/version\n")
    time.sleep(1)
    line = client.console_head() # Prompt + command
    line = client.console_head() # Command output (1st line)
    if line is not None and line.startswith("Linux "):
        step.context.runtime = "Linux"
    assert step.context.runtime == "Linux"

@step("Linux was booted")
def linux_booted(step):
    step.behave_like("my target is on")
    step.behave_like("Linux is running")

@given("my USB {className:w} device is detached")
def usb_device_detached(step, className):
    client = step.context.client
    step.context.usb_device_class = className

    available = client.usb_has_class(className)
    if available == False:
        step.pending()
    else:
        # Detach the specified device
        offline = client.usb_off_by_class(className)
        assert offline == True

        # Give the runtime plenty of time to detect removal of the USB device
        time.sleep(1)

@when("I attach my USB {className:w} device")
def attach_usb_device(step, className):
    client = step.context.client
    step.context.usb_device_class = className

    available = client.usb_has_class(className)
    if available == False:
        step.pending()
    else:
        # Detach the specified device
        online = client.usb_on_by_class(className)
        assert online == True

        # Give the runtime plenty of time to detect the USB device
        time.sleep(5)

@given("I have noted available disks")
def note_available_disks(step):
    client = step.context.client

    # Check for target console
    online = console_login(client)
    assert online == True

    # Get available disks
    results = client.console_run("cat /proc/diskstats|awk '{ print $3; }'")
    step.context.disks = results.split('\n')[1:-1]

@then("I expect new disk(s)")
def expect_new_disks(step):
    client = step.context.client

    # Check for target console
    online = console_login(client)
    assert online == True

    # Get available disks
    results = client.console_run("cat /proc/diskstats|awk '{ print $3; }'")
    disks = results.split('\n')[1:-1]

    assert step.context.disks is not None
    assert len(disks) > len(step.context.disks)

def console_check(client):

    line  = None
    tries = 3

    while line is None and tries > 0:
        client.console_clear()
        client.console_send("\3\n")
        time.sleep(1)
        line = client.console_tail()
        tries = tries - 1

    return line is not None

def console_prompt(client):

    online = False
    tries  = 3

    client.console_prompt("# ")

    while online == False and tries > 0:
        client.console_clear()
        client.console_send("\3\n")
        time.sleep(1)
        line = client.console_tail()
        if line is not None and line.endswith("# "):
            online = True
        tries = tries - 1

    return online

def console_login(client):

    # Check for target console
    online = console_check(client)
    assert online == True

    # Check if we need to login
    client.console_send("\3\n")
    time.sleep(1)
    line = client.console_tail()
    if line is not None and line.endswith("login: "):
        client.console_send("root\n")
        time.sleep(1)

    online = console_prompt(client)
    return online

def target_on(client):
    # Acquire the board
    status = client.target_lock(30)
    if status == False:
        return False

    # If the board is currently switched OFF
    if client.target_status() == "OFF":
        # Attach the SD card back to the board and power it
        status = client.sd_to_target()
        if status == False:
            return False
        time.sleep(3)
        status = client.target_on()
    return status

def target_off(client):
    # Acquire the board
    status = client.target_lock(30)
    if status == False:
        return False

    # Switch the board OFF
    if client.target_status() == "ON":
        status = client.target_off()
        if status == False:
            return False
        time.sleep(3)

    # Attach the SD card back to the host
    return client.sd_to_host()
