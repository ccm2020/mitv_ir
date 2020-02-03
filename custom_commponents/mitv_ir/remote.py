"""Support for iTach IR devices."""
import logging
import voluptuous as vol
import socket
import binascii
import os

from homeassistant.components import remote
from homeassistant.components.remote import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    DEVICE_DEFAULT_NAME,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 6091
CONNECT_TIMEOUT = 5000


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port
    }
)

comm_home = "040041010000000b003a0100000000020000000003000000030400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_back = "040041010000000b003a0100000000020000000003000000040400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_menu = "040041010000000b003a0100000000020000000003000000520400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_off = "040041010000000b003a01000000000200000000030000001a0400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_up = "040041010000000b003a0100000000020000000003000000130400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_down = "040041010000000b003a0100000000020000000003000000140400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_left = "040041010000000b003a0100000000020000000003000000150400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_right = "040041010000000b003a0100000000020000000003000000160400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_enter = "040041010000000b003a0100000000020000000003000000170400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_volup = "040041010000000b003a0100000000020000000003000000180400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"
comm_voldown = "040041010000000b003a0100000000020000000003000000190400000000050000000006000000000700000000000000000800000000000000000affffffff0b00000000"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the ITach connection and devices."""

    serv_host = config.get('host')
    serv_port = config.get('port')
    serv_name = config.get('name')

    devices = [MITVIRRemote(serv_host,serv_port,serv_name)]
    add_entities(devices, True)
    return True


class MITVIRRemote(remote.RemoteDevice):
    """Device that sends commands to an ITachIP2IR device."""

    def __init__(self, host, port, name):
        """Initialize device."""
        self._host = host
        self._port = port or DEFAULT_PORT
        self._name = name or DEVICE_DEFAULT_NAME

    @property
    def name(self):
        """Return the name of the device."""
        return self._name
    @property
    def state(self):
        """Return the state."""
        return self._state
    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def send_command(self, command, **kwargs):
        """Send a command to one device."""
        if self._state == 'off':
            return False
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.connect((self._host ,self._port))
        for single_command in command:
            if(single_command == 'home'):
                self._server.send(binascii.a2b_hex(comm_home))
            if(single_command == 'back'):
                self._server.send(binascii.a2b_hex(comm_back))
            if(single_command == 'menu'):
                self._server.send(binascii.a2b_hex(comm_menu))
            if(single_command == 'poweroff'):
                self._server.send(binascii.a2b_hex(comm_off))
            if(single_command == 'up'):
                self._server.send(binascii.a2b_hex(comm_up))
            if(single_command == 'down'):
                self._server.send(binascii.a2b_hex(comm_down))
            if(single_command == 'left'):
                self._server.send(binascii.a2b_hex(comm_left))
            if(single_command == 'right'):
                self._server.send(binascii.a2b_hex(comm_right))
            if(single_command == 'enter'):
                self._server.send(binascii.a2b_hex(comm_enter))
            if(single_command == 'volup'):
                self._server.send(binascii.a2b_hex(comm_volup))
            if(single_command == 'voldown'):
                self._server.send(binascii.a2b_hex(comm_voldown))
        self._server.close()
    def update(self):
        """Update the device."""
        res = os.system('ping -c 1 -W 5 '+self._host)
        if res == 0:
            self._state = 'on'
        else:
            self._state = 'off'
        return self._state