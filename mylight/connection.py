import asyncio
import functools
import logging
from enum import Enum
from typing import Any, Callable
from uuid import UUID
from mylight import const, protocol


from bleak import BleakClient, BleakError, BleakScanner
from bleak.backends.client import BaseBleakClient
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection

_LOGGER = logging.getLogger(__name__)

RECIVE_UUID: UUID = "0000a041-0000-1000-8000-00805f9b34fb"
CONTROL_UUID: UUID = "0000a040-0000-1000-8000-00805f9b34fb"
NAME_UUID: UUID = "00002a00-0000-1000-8000-00805f9b34fb"
NOTIFY_HANDLE: hex = 0x8


class Conn(Enum):
    CONNECTED = 0
    DISCONNECTED = 1


def connection_required(func):
    """Raise an exception before calling the actual function if the device is
    not connected.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._client is None:
            raise Exception("Not connected")

        return func(self, *args, **kwargs)

    return wrapper


def model_from_name(ble_name: str) -> str:
    model = "Mylight"
    return model


async def find_device_by_address(
    address: str, timeout: float = 20.0
) -> BLEDevice:
    from bleak import BleakScanner

    return await BleakScanner.find_device_by_address(address.upper(), timeout=timeout)


async def discover_mylight_lamps(
    scanner: type[BleakScanner],
) -> list[dict[str, Any]]:
    """Scanning feature
    Scan the BLE neighborhood for an Yeelight lamp
    This method requires the script to be launched as root
    Returns the list of nearby lamps
    """
    lamp_list = []
    scanner = scanner if scanner is not None else BleakScanner

    devices = await scanner.discover()
    for d in devices:
        model = model_from_name(d.name)
    return lamp_list


class Connection():
    def __init__(self, ble_device: BLEDevice, timeout: int, retries: int) -> None:
        self._client: BleakClient | None = None
        self._ble_device = ble_device
        self._mac = self._ble_device.address
        _LOGGER.debug(
            f"Initializing MyLight Lamp {self._ble_device.name} ({self._mac})"
        )
        self._timeout = timeout
        self._retries = retries
        self._state_callbacks: list[Callable[[], None]] = []
        self._read_service = False
        self._conn = Conn.DISCONNECTED

    def add_callback_on_state_changed(self, func: Callable[[], None]) -> None:
        """
        Register callbacks to be called when lamp state is received or bt disconnected
        """
        self._state_callbacks.append(func)

    def run_state_changed_cb(self) -> None:
        """Execute all registered callbacks for a state change"""
        for func in self._state_callbacks:
            func()

    def diconnected_cb(self, client: BaseBleakClient) -> None:
        # ensure we are responding to the newest client:
        if client != self._client:
            return
        _LOGGER.debug(
            f"Client with address {client.address} got disconnected!")
        self._conn = Conn.DISCONNECTED
        self.run_state_changed_cb()

    async def connect(self, num_tries: int = 3) -> None:
        _LOGGER.debug("Initiating new connection")
        try:
            if self._client:
                await self.disconnect()

            _LOGGER.debug("Connecting now:...")
            self._client = await establish_connection(
                BleakClient,
                device=self._ble_device,
                name=self._mac,
                disconnected_callback=self.diconnected_cb,
                max_attempts=3,
            )
            _LOGGER.debug(f"Connected: {self._client.is_connected}")

            # read services if in debug mode:
            if not self._read_service and _LOGGER.isEnabledFor(logging.DEBUG):
                await self.read_services()
                self._read_service = True
                await asyncio.sleep(0.2)

            _LOGGER.debug("Request Notify")
            await self._client.start_notify(NOTIFY_HANDLE, self.notification_handler)
            await asyncio.sleep(0.3)
            await self.get_services()
            self._conn == Conn.CONNECTED

            _LOGGER.debug(f"Connection status: {self._conn}")

        except asyncio.TimeoutError:
            _LOGGER.error("Connection Timeout error")
        except BleakError as err:
            _LOGGER.error(f"Connection: BleakError: {err}")

    async def disconnect(self) -> None:
        if self._client is None:
            return
        try:
            await self._client.disconnect()
        except asyncio.TimeoutError:
            _LOGGER.error("Disconnection: Timeout error")
        except BleakError as err:
            _LOGGER.error(f"Disconnection: BleakError: {err}")
        self._conn = Conn.DISCONNECTED

    def notification_handler(self, sender, data):
        """Simple notification handler which prints the data received."""
        print("Notification {0}: {1}".format(sender, data))
        self.run_state_changed_cb()

    def is_connected(self) -> bool:
        """
        :return: True if connected
        """
        return self._client.is_connected

    async def test_connection(self) -> bool:
        """
        Test if the connection is still alive

        :return: True if connected
        """
        if self.is_connected():
            return True

        await self.disconnect()
        await asyncio.sleep(2.0)

        # reconnect and send test message, read bulb name
        try:
            await self.connect(num_tries=10)
            await asyncio.sleep(0.7)
            await self.get_device_name()
            await asyncio.sleep(0.7)
        except BleakError:
            self.disconnect()
            await asyncio.sleep(2.0)
            return False
        except BrokenPipeError:
            self._client = None
            return False

        return True

    async def get_services(self) -> None:
        """
        :return: Services
        """
        svcs = await self._client.get_services()
        print("Services:")
        for service in svcs:
            print(service)

    async def get_device_name(self) -> str:
        """
        :return: Device name
        """
        buffer: bytearray = await self.read_cmd(NAME_UUID)
        return buffer.decode('utf-8')

    async def get_category_info(self, category, functions) -> list:
        """
        Retrieve category in from all functions.

        :param category: category to retrieve info from
        :param functions: functions to retrieve info from
        """
        buffer_list = []
        for func in functions:
            msg = protocol.encode_msg(category.value,
                                      func.value,
                                      const.Commands.REQ_DATA.value)
            await self.send_cmd(msg)
            buffer = await self.read_cmd()
            _LOGGER.debug(buffer)
            buffer_list.append(protocol.decode_function(buffer))
            self.run_state_changed_cb()
        return buffer_list

    def validate_response(self, rsp) -> bool:
        if rsp['rsp'] == ['wr']:
            return True
        return False

    async def send_cmd(self, msg: bytearray, UUID: UUID = CONTROL_UUID):
        if self.test_connection():
            await self._client.write_gatt_char(UUID, msg, response=True)

    async def read_cmd(self, UUID: UUID = RECIVE_UUID) -> bytearray:
        if self.test_connection():
            return await self._client.read_gatt_char(UUID, respone=True)
        return None

    async def find_device_by_address(
        address: str, timeout: float = 20.0
    ) -> BLEDevice:
        from bleak import BleakScanner

        return await BleakScanner.find_device_by_address(address.upper(), timeout=timeout)
