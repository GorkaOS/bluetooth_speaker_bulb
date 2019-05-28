# MyLight Bulb
Use at own risk! This library is only for the settings of the bulb, not playing music.

## Mylight Bulb
<img src="https://cdn.shopify.com/s/files/1/1026/2915/products/71sjF1R7SnL._SL1500_1024x1024.jpg?v=1499116245" width="200">


## Usage
### Module

```python
from mylight import MyLight
from time import sleep
import logging
logging.basicConfig(level=logging.DEBUG)

bulb = MyLight('00:00:00:00:00:00', 0)
bulb.connect()
bulb.is_on

bulb.set_effect('music')
for i in range(100):
    bulb.set_sound_level(i)

sleep(1)

bulb.get_device_info()
bulb.effect_value
bulb.effect_name
bulb.effect


bulb.test_connection()
bulb.turn_on()

for i in range(5):
    bulb.test_connection()
    bulb.is_on
    bulb.turn_on
    bulb.is_on
    bulb.turn_off()
    bulb.is_on

bulb.turn_on()
bulb.set_brightness(50)
sleep(1)
bulb.set_brightness(100)
sleep(1)
bulb.set_brightness(150)
sleep(1)
bulb.set_brightness(200)
sleep(1)
bulb.set_brightness(250)
sleep(1)
bulb.set_brightness(255)

sleep(1)

bulb.turn_off()
bulb.turn_on()
for i in range(10):
    bulb.set_random_color()
    sleep(1)


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

### Receive (sound and timer, lamp has no response) <br>
{4 byte} header [0x55, 0xaa] <br>
{2 byte} data length <br>
{2 byte} 0x88 lamp/effect, 0x85 timer, 0x84 music/sound settings <br>
{2 byte} function <br>
{data length byte} data <br>
{2 byte} checksum <br>

# Credits / Special Thanks
* https://github.com/Betree