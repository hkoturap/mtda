Configuration
=============

MTDA will reads it configuration from:

 * $HOME/.mdta/config
 * /etc/mtda/config

Configuration files are similar to what’s found in Microsoft Windows INI
files (Python's `configparser` module is used to parse them).

It is possible to override some settings using environment variables.

General settings
----------------

* ``main``: section [optional]
    Usually placed at the top of MTDA configuration files. It contains general
    settings.

  * ``debug``: integer [optional]
      Level of debug messages to print out while running (set to 0 to turn all
      debug messages off).

  * ``fuse``: boolean [optional]
      Enable support for mounting partitions from the shared device using FUSE
      instead of ``losetup`` and ``mount``. This feature is experimental and
      requires ``partitionfs``, ``fuseext2`` and ``fusefat``.

* ``ui``: section [optional]
  User Interface settings for the console. This is relevant only for MTDA clients.

  * ``prefix``: string [optional]
      Change the key prefix to control the interactive MTDA console. The default
      prefix is ``ctrl-a`` (which is also used by the ``screen`` tool, this
      setting may be used to use e.g. ``ctrl-b`` instead).

* ``console``: section [optional]
    Specify console settings when running the agent-side of MTDA (this section
    is ignored when running MTDA as a client). The ``variant`` key should be
    set, other settings in this section are variant-specific.

  * ``variant``: string [required]
      Select a console variant. MTDA provides the following drivers: ``serial``
      and ``telnet``.

* ``keyboard``: section [optional]
    Specify a keyboard driver.

  * ``variant``: string [required]
      Select a keyboard driver between ``hid`` and ``qemu``.

* ``power``: section [optional]
    Configure a power controller for the device attached to MTDA. The driver
    may be selected with ``variant``.

  * ``variant``: string [required]
      Select a power variant from ``aviosys_8800``, ``gpio``, ``pduclient`` and
      ``qemu``.

* ``remote``: section [optional]
    Specify the host and ports to connect to when using a MTDA client (such as
    ``mtda-cli``).

  * ``control``: integer [optional]
      Remote port listening for control commands (defaults to ``5556``).

  * ``console``: integer [optional]
      Remote port to connect to in order to get console messages (defaults to
      ``5557``).

  * ``host``: string [optional]
      Remote host name or ip to connect to as a client to interact with the
      MTDA agent (defaults to ``localhost``).

* ``scripts``: section [optional]
    Python scripts to be executed upon certain events. Use ``... `` instead of
    hard/soft spaces.

  * ``power off``: string [optional]
      Execute a Python script when the device is powered off.
     
  * ``power on``: string [optional]
      Execute a Python script when the device is powered on.
     
* ``sdmux``: section [optional]
    Configure a shared storage driver that may be swapped between the device
    attached to MTDA and the host running the agent. The driver will be
    selected with ``variant``.

  * ``variant``: string [required]
      Select a sdmux variant from ``qemu``, ``samsung`` and ``usbf``.

* ``usb``: section [optional]
    Specify how many USB ports may be controlled from this agent.

  * ``ports``: integer [optional]
      Number of USB ports. Each port should then be configured with its own
      ``[usbN]`` section where ``N`` is the port index (starting from ``1``).

Console settings
----------------

The ``[console]`` section configures the console for interacting with the
device to the MTDA agent. The driver is selected with the ``variant``
setting. Options specific to each driver are documented below.

``qemu`` driver settings
~~~~~~~~~~~~~~~~~~~~~~~~

Use the ``qemu`` console driver when the power driver is also set to ``qemu``.
This driver will interact with the emulated serial device. There are no further
settings for this driver.

``serial`` driver settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``serial`` driver may be used when the device uses a serial console. The
following may be configured:

* ``port``: string [required]
    Path to the serial device on the host running the MTDA agent (for
    example /dev/ttyS0).

* ``rate``: integer [optional]
    The baud rate used by the device to communicate with the MTDA agent. This
    setting defaults to ``115200``.

``telnet`` driver settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

Some power distribution racks also include serial interfaces that are exposed
to remote clients via telnet. Some debug boards may also be attached to custom
hardware designs. The ``telnet`` driver may be used in such configurations and
supports the following settings:

* ``host``: string [required]
    Hostname of the telnet server.

* ``port``: integer [optional]
    The port on which the telnet server is running (defaults to ``23``).

* ``delay``: integer [optional]
    Time interval (in seconds) to wait for before trying to reconnect to the
    telnet server (defaults to 5 seconds).

* ``timeout``: integer [optional]
    Timeout (in seconds) for each connect.

Power settings
--------------

The ``[power]`` section configures a power controller to power the device on or
off. The driver is selected with the ``variant`` setting. Driver-specific
settings are detailed below.

``aviosys_8800`` driver settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``aviosys_8800`` driver supports the USB controller power outlet from
Aviosys. The following settings are supported:

* ``pid``: integer [optional]
    The USB product ID of the power outlet (defaults to ``2303``).

* ``vid``: integer [optional]
    The USB vendor ID of the power outlet (defaults to ``067b``).

``gpio`` driver settings
~~~~~~~~~~~~~~~~~~~~~~~~

The ``gpio`` driver may be used to control a simple electric relay using GPIO
lines from the system running the MTDA agent. The following settings are
supported:

* ``pin``: integer [required]
    Specify the GPIO pin number to be used to control the relay.

``pduclient`` driver settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``pduclient`` driver may be used to let a LAVA instance control the power
of the device attached to MTDA. The following settings are supported:

* ``daemon``: string [required]
    Determines the hostname of the hostname which is running ``lavapdu-listen``
    to which the MTDA agent can connect to and send power commands.

* ``hostname``: string [required]
    The PDU which will run power commands sent by the MTDA agent.

* ``port``: integer [required]
    The port on the specified PDU to which the device is connected.

``qemu`` driver settings
~~~~~~~~~~~~~~~~~~~~~~~~

The ``qemu`` driver may be used to use QEMU/KVM instead of a physical device.
The following settings are supported:

* ``bios``: string [optional]
    The BIOS to be loaded by QEMU/KVM.

* ``cpu``: string [optional]
    The CPU to be emulated by QEMU/KVM.

* ``executable``: string [optional]
    The QEMU/KVM executable to use as system emulator. This setting defaults
    to ``kvm``

* ``hostname``: string [optional]
    Name of emulated machine to be provided by QEMU/KVM internal DHCP server.

* ``machine``: string [optional]
    The QEMU/KVM machine to emulate.

* ``memory``: integer [optional]
    The amount of memory (in mega-bytes) for the emulated machime (defaults to
    512 MiB).

* ``pflash_ro``: string [optional]
    Path to the read-only firmware flash.

* ``pflash_rw``: string [optional]
    Path to the read-write firmware flash.

* ``storage``: string [optional]
    Path to the emulated machine storage.

* ``swtpm``: string [optional]
    Path to the ``swtpm`` binary to support emulation of a TPM device.

* ``watchdog``: string [optional]
    Name of the watchdog driver provided by QEMU/KVM for the selected machine.

Shared device settings
----------------------

The ``[sdmux]`` section configures a shared storage device that may be used
either from the device under test or from the host running the MTDA agent. The
driver is selected with the ``variant`` setting. Driver-specific settings are
detailed below.

``samsung`` driver settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``samsung`` driver supports both SD Mux and SD Wire and may used to share
a SD card between the DUT and host. The following settings are supported:

* ``device``: string [optional]
  Block device for the shared SD card as seen on the host (defaults to
  ``/dev/sda``)

* ``serial``: string [optional]
  Identifier of the sdmux/sdwire device to use (defaults to ``sdmux``). Use
  ``sd-mux-ctrl`` to list available devices.
