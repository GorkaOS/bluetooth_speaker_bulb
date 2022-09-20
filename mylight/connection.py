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

MODEL_MYLIGHT = "MyLight"
MODEL_UNKNOWN = "Unknown"


class Conn(Enum):
    CONNECTED = 0
    DISCONNECTED = 1


def model_from_name(ble_name: str) -> str:
    model = MODEL_UNKNOWN
    if ble_name.startswith("MyLight"):
        model = MODEL_MYLIGHT
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
    Scan the BLE neighborhood for an MyLight lamp
    This method requires the script to be launched as root
    Returns the list of nearby lamps
    """
    lamp_list = []
    scanner = scanner if scanner is not None else BleakScanner

    devices = await scanner.discover()
    for d in devices:
        model = model_from_name(d.name)
        if model != MODEL_UNKNOWN:
            lamp_list.append({"ble_device": d, "model": model})
            _LOGGER.info(
                f"found {model} with mac: {d.address}, details:{d.details}")
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

            _LOGGER.debug(f"Connection status: Connected")

        except asyncio.TimeoutError:
            _LOGGER.error("Connection Timeout error")
        except BleakError as err:
            _LOGGER.error(f"Connection: BleakError: {err}")

    async def disconnect(self) -> None:
        if self._client is None:
            return
        try:
            await self._client.disconnect()
            asyncio.sleep(5.0)
        except asyncio.TimeoutError:
            _LOGGER.error("Disconnection: Timeout error")
        except BleakError as err:
            _LOGGER.error(f"Disconnection: BleakError: {err}")
        self._client = None

    def notification_handler(self, sender, data):
        """Simple notification handler which prints the data received."""
        print("Notification {0}: {1}".format(sender, data))
        self.run_state_changed_cb()

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
            if buffer:
                _LOGGER.debug(
                    f"Connection get_category_info, buffer: {buffer}")
                buffer_list.append(protocol.decode_function(buffer))
            else:
                _LOGGER.debug(
                    f"Connection get_category_info, buffer empty, buffer {buffer}")
                buffer_list = None
                break

        self.run_state_changed_cb()
        return buffer_list

    async def test_connection(self) -> bool:
        _LOGGER.debug(f"Test Connection")
        if self._client:
            if self._client.is_connected:
                try:
                    await self.get_device_name
                    await asyncio.sleep(0.1)
                except asyncio.TimeoutError:
                    _LOGGER.error("Test Connection: Timeout error")
                except BrokenPipeError as err:
                    _LOGGER.error(f"Test Connection: BrokenPipeError: {err}")
                except BleakError as err:
                    _LOGGER.error(f"Test Connection: BleakError: {err}")
                return True
            await self.disconnect()
        return False

    async def send_cmd(self, msg: bytearray, UUID: UUID = CONTROL_UUID, wait_notif: float = 0.5) -> bool:
        if not await self.test_connection():
            await self.connect()
        try:
            await self._client.write_gatt_char(UUID, msg, response=True)
            await asyncio.sleep(wait_notif)
            return True
        except asyncio.TimeoutError:
            _LOGGER.error("Send Cmd: Timeout error")
        except BleakError as err:
            _LOGGER.error(f"Send Cmd: BleakError: {err}")
        return False

    async def read_cmd(self, UUID: UUID = RECIVE_UUID) -> bytearray:
        if not await self.test_connection():
            await self.connect()
        try:
            return await self._client.read_gatt_char(UUID, respone=True)
        except asyncio.TimeoutError:
            _LOGGER.error("Read Cmd: Timeout error")
        except BleakError as err:
            self.disconnect()
            _LOGGER.error(f"Read Cmd: BleakError: {err}")

    async def find_device_by_address(
        address: str, timeout: float = 20.0
    ) -> BLEDevice:
        from bleak import BleakScanner

        return await BleakScanner.find_device_by_address(address.upper(), timeout=timeout)

    async def read_services(self) -> None:
        if self._client is None:
            return
        for service in self._client.services:
            _LOGGER.info(f"[Service] {service}")
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await self._client.read_gatt_char(char.uuid))
                        _LOGGER.info(
                            f"__[Characteristic] {char} ({','.join(char.properties)}), Value: {str(value)}"
                        )
                    except Exception as e:
                        _LOGGER.error(
                            f"__[Characteristic] {char} ({','.join(char.properties)}), Value: {e}"
                        )

                else:
                    value = None
                    _LOGGER.info(
                        f"__[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                    )

                for descriptor in char.descriptors:
                    try:
                        value = bytes(
                            await self._client.read_gatt_descriptor(descriptor.handle)
                        )
                        _LOGGER.info(
                            f"____[Descriptor] {descriptor}) | Value: {str(value)}"
                        )
                    except Exception as e:
                        _LOGGER.error(
                            f"____[Descriptor] {descriptor}) | Value: {e}")
