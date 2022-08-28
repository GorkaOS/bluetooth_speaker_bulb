
import functools
import logging
from bluepy import btle
from enum import Enum
from mylight import bulb, const, protocol

logger = logging.getLogger(__name__)


class UUID_CHARACTERISTIC(Enum):
    """
    An enum of all UUID Characteristics
    """
    RECV = "0000a041-0000-1000-8000-00805f9b34fb"
    WRITE = "0000a040-0000-1000-8000-00805f9b34fb"
    DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb"


def connection_required(func):
    """Raise an exception before calling the actual function if the device is
    not connected.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._connection is None:
            raise Exception("Not connected")

        return func(self, *args, **kwargs)

    return wrapper


def _figure_addr_type(mac_address=None, addr_type=None):
    # addr_type rules all
    if addr_type is not None:
        return addr_type

    # try using mac_address
    if mac_address is not None:
        mac_address_num = int(mac_address.replace(':', ''), 16)
        if mac_address_num & 0xF00000000000 == 0xF00000000000:
            return btle.ADDR_TYPE_PUBLIC

    return btle.ADDR_TYPE_PUBLIC


class Connection():

    def __init__(self, mac_address, adapter, retries=3) -> None:
        self._retries = retries
        self._mac_address = mac_address
        self._adapter = adapter
        self._connection = None
        self._addr_type = btle.ADDR_TYPE_PUBLIC
        self.connect()

    def connect(self):
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
                connection = btle.Peripheral(
                    self._mac_address, self._addr_type, self._adapter)
                self._connection = connection.withDelegate(self)
                self._subscribe_to_recv_characteristic()
            except btle.BTLEException as e:
                if e.code != btle.BTLEException.DISCONNECTED:
                    raise
            else:
                logger.info(
                    'Successfully connected to: {}'.format(self._mac_address))
                break

            if attempt == self._retries:
                logger.error('Connection failed: {}'.format(
                    self._mac_address))
                return False
        return True

    def disconnect(self):
        """
        Disconnect from device
        """
        logger.debug("Disconnecting...")

        try:
            self._connection.disconnect()
        except btle.BTLEException:
            pass

        self._connection = None

    def is_connected(self):
        """
        :return: True if connected
        """
        return self._connection is not None

    def test_connection(self):
        """
        Test if the connection is still alive

        :return: True if connected
        """
        if not self.is_connected():
            return False

        # send test message, read bulb name
        try:
            self.get_device_name()
        except btle.BTLEException:
            self.disconnect()
            return False
        except BrokenPipeError:
            # bluepy-helper died
            self._connection = None
            return False

        return True

    @connection_required
    def get_device_name(self):
        """
        :return: Device name
        """
        buffer = self._device_name_characteristic.read()
        buffer = buffer.replace(b'\x00', b'')
        return buffer.decode('ascii')


    @connection_required
    def get_category_info(self, category, functions):
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
            # msg.append(protocol.encode_checksum(msg))
            self.send_message(msg)
            buffer = self.read_message()
            logger.debug(buffer)
            buffer_list.append(protocol.decode_function(buffer))
        return buffer_list

    def validate_response(self, rsp) -> bool:
        if rsp['rsp'] == ['wr']:
            return True
        return False

    @connection_required
    def send_message(self, msg) -> bool:
        return self.validate_response(self._send_characteristic.write(msg, withResponse=True))

    @connection_required
    def read_message(self):
        return self._connection.readCharacteristic(0x000e)


    @property
    def _send_characteristic(self):
        """Get BTLE characteristic for sending commands"""
        characteristics = self._connection.getCharacteristics(
            uuid=UUID_CHARACTERISTIC.WRITE.value)
        if not characteristics:
            return None
        return characteristics[0]

    @property
    def _recv_characteristic(self):
        """Get BTLE characteristic for receiving data"""
        characteristics = self._connection.getCharacteristics(
            uuid=UUID_CHARACTERISTIC.RECV.value)
        if not characteristics:
            return None
        return characteristics[0]

    @property
    def _device_name_characteristic(self):
        """Get BTLE characteristic for reading device name"""
        characteristics = self._connection.getCharacteristics(
            uuid=UUID_CHARACTERISTIC.DEVICE_NAME.value)
        if not characteristics:
            return None
        return characteristics[0]

    @property
    def _light_info_characteristic(self):
        """Get BTLE characteristic for reading device name"""
        characteristics = self._connection.getCharacteristics(
            uuid=UUID_CHARACTERISTIC.RECV.value)
        if not characteristics:
            return None
        return characteristics[0]

    def _subscribe_to_recv_characteristic(self):
        char = self._recv_characteristic
        handle = char.valHandle - 4
        msg = bytearray([0x01, 0x00])
        self._connection.writeCharacteristic(handle, msg, withResponse=True)
