# Alloyseed Speaker Bulb (MyLight?)
Use at own risk! This library is only for the settings of the bulb, not playing music.

## Alloyseed Bulb
<img src="https://cdn.shopify.com/s/files/1/1026/2915/products/71sjF1R7SnL._SL1500_1024x1024.jpg?v=1499116245" width="200">


## Usage
### Module

```python
import asyncio
import logging
from alloyseed.bulb import Bulb

logging.basicConfig(level=logging.DEBUG)

ADDRESS = "00:00:00:00:00:00"
ADAPTER = "hci0"


async def main(target_mac_address, host_adapter):
    bulb = Bulb(mac_address=target_mac_address, adapter=host_adapter)
    print(await bulb.connect())

    await bulb.update()
    print(await bulb.get_device_name())
    await bulb._connection.get_services()

    await bulb.turn_off()
    for k in range(1, 10, 1):
        print(await bulb.get_light_info())
        print(await bulb.turn_on())
        await bulb.turn_on(20*k)
        await asyncio.sleep(0.1)

    await bulb.update_light()

    await bulb.set_volume(50)

    await bulb.set_speaker_effect('flat')
    await bulb.update_speaker()
    print(bulb._speaker.effect)
    await asyncio.sleep(2)

    await bulb.set_speaker_effect('classical')
    await bulb.update_speaker()
    print(bulb._speaker.effect)
    await asyncio.sleep(2)

    await bulb.set_speaker_effect('pop')
    await bulb.update_speaker()
    print(bulb._speaker.effect)
    await asyncio.sleep(2)

    await bulb.set_speaker_effect('bass')
    await bulb.update_speaker()
    print(bulb._speaker.effect)
    await asyncio.sleep(2)

    await bulb.set_speaker_effect('jazz')
    await bulb.update_speaker()
    print(bulb._speaker.effect)
    await asyncio.sleep(2)

    print(await bulb.disconnect())


asyncio.run(main(ADDRESS, ADAPTER))

```

# Todo
See [List](TODO.md)

## Package description
### Send <br>
{4 byte} header [0x55, 0xaa] <br>
{2 byte} data length <br>
{2 byte} 0x08 lamp/effect, 0x05 timer, 0x04 music/sound settings <br>
{2 byte} function <br>
{data length byte} data <br>
{2 byte} checksum <br>

### Receive <br>
{4 byte} header [0x55, 0xaa] <br>
{2 byte} data length <br>
{2 byte} 0x88 lamp/effect, 0x85 timer, 0x84 music/sound settings <br>
{2 byte} function <br>
{data length byte} data <br>
{2 byte} checksum <br>

# Credits / Special Thanks
* https://github.com/Betree
