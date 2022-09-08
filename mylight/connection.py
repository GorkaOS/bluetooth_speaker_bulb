import functools
import logging
from typing import Any
from uuid import UUID
from mylight import const, protocol


from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError, BleakDBusError
from bleak.backends.device import BLEDevice

logger = logging.getLogger(__name__)

RECIVE_UUID: UUID = "0000a041-0000-1000-8000-00805f9b34fb"
CONTROL_UUID: UUID = "0000a040-0000-1000-8000-00805f9b34fb"
NAME_UUID: UUID = "00002a00-0000-1000-8000-00805f9b34fb"
NOTIFY_HANDLE: hex = 0x8

def connection_required(func):
    """Raise an exception before calling the actual function if the device is
    not connected.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._client.is_connected:
            raise Exception("Not connected")

        return func(self, *args, **kwargs)

    return wrapper

def model_from_name(ble_name: str) -> str:
    model = "Mylight"
    # if ble_name.startswith("XMCTD_"):
    #     model = MODEL_BEDSIDE
    # if ble_name.startswith("yeelight_ms"):
    #     model = MODEL_CANDELA
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

    # def __init__(self, mac_address: str, adapter: str, timeout: int, retries: int) -> None:
    def __init__(self, ble_device: BLEDevice, timeout: int, retries: int) -> None:
        self._ble_device = ble_device
        self._mac_address = ble_device.address
        # self._adapter = adapter
        self._timeout = timeout
        self._retries = retries
        self._client = BleakClient(
            self._ble_device, timeout=self._timeout)

    def notification_handler(sender, data):
        """Simple notification handler which prints the data received."""
        print("Notification {0}: {1}".format(sender, data))

    async def connect(self) -> bool:
        """
        Connect to device

        :param adapter: bluetooth adapter name as shown by\
            "hciconfig" command. Default : 0 for (hci0)

        :return: True if connection succeed, False otherwise
        """
        logger.debug("Connecting...")
        for attempt in range(1, self._retries + 1, 1):
            logger.info('Connection attempt: {}'.format(attempt))

            try:
                await self._client.connect()
                await self._client.start_notify(NOTIFY_HANDLE, self.notification_handler)
            except BleakError:
                pass
            else:
                logger.info(
                    'Successfully connected to: {}'.format(self._mac_address))
                break
        if attempt == self._retries:
            logger.error('Connection failed: {}'.format(
                self._mac_address))

        return self._client.is_connected

    async def disconnect(self) -> bool:
        """
        Disconnect from device
        """
        logger.debug("Disconnecting...")

        try:
            await self._client.disconnect()
        except BleakError:
            pass
        return not self._client.is_connected

    def is_connected(self) -> bool:
        """
        :return: True if connected
        """
        return self._client.is_connected

    def test_connection(self) -> bool:
        """
        Test if the connection is still alive

        :return: True if connected
        """
        if not self.is_connected():
            return False

        # send test message, read bulb name
        try:
            self.get_device_name()
        except BleakError:
            self.disconnect()
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
            logger.debug(buffer)
            buffer_list.append(protocol.decode_function(buffer))
        return buffer_list

    def validate_response(self, rsp) -> bool:
        if rsp['rsp'] == ['wr']:
            return True
        return False

    # @connection_required
    async def send_cmd(self, msg: bytearray, UUID: UUID = CONTROL_UUID):
        if not self.is_connected:
            await self.connect()
        await self._client.write_gatt_char(UUID, msg, response=True)

    # @connection_required
    async def read_cmd(self, UUID: UUID = RECIVE_UUID) -> bytearray:
        if not self.is_connected:
            await self.connect()
        return await self._client.read_gatt_char(UUID, respone=True)

    async def find_device_by_address(
        address: str, timeout: float = 20.0
    ) -> BLEDevice:
        from bleak import BleakScanner

        return await BleakScanner.find_device_by_address(address.upper(), timeout=timeout)
