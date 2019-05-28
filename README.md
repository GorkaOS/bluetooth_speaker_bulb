# MyLight Bulb, based on [MagicBlue](https://github.com/Betree/magicblue) by Betree
Use at own risk! This library is only for the settings of the bulb, not bt-music playing.

## Mylight Bulb
<img src="https://cdn.shopify.com/s/files/1/1026/2915/products/71sjF1R7SnL._SL1500_1024x1024.jpg?v=1499116245" width="500">

Please visit Betrees repository for more info [magicblue](https://github.com/Betree/magicblue)


## Example use:

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



## Todo

### Todo for MyLight Bulb <br>
[ ] Fix magicblueshell for both magicblue and mylight <br>
[x] Encode <br>
[x] Encode all messages of one func <br>
[x] Checksum send <br>
[x] Checksum receive <br>
[x] Current status <br>
[?] Decode response status <br>
[x] Decode response lamp <br>
[x] Test response lamp <br>
[x] Decode response timer <br>
[ ] Test response timer <br>
[x] Decode response sound <br>
[ ] Test response sound <br>
[x] Receive response when write-req <br>
[x] On/off <br>
[x] Colors <br>
[x] Effects <br>
[x] Brightness/Warm <br>
[x] White (special effect, no good solution yet) <br>
[x] White is it possible to set temp?
[x] White status
[x] Sound equalizer mode, not tested <br>
[x] Sound equalizer settings, not tested <br>
[x] Sound Volume, not tested <br>
[x] Time/Alarm, not tested <br>
[-] Pull-req to Betree (if possible) <br>

### Todo Home assistant 
[x] Home assistant custom_component [repo](https://github.com/orrpan/homeassistant-magicblue)<br>
[x] On/Off<br>
[x] Brightness<br>
[x] RGB <br>
[x] Effects <br>
[x] White <br>
[x] Get updates from bulb <br>
[-] Timer, not needed <br>
[ ] Music, maybe not needed <br>

### Package description
#### Send <br>
{4 byte} header [0x55, 0xaa] <br>
{2 byte} data length <br>
{2 byte} 0x08 lamp/effect, 0x05 timer, 0x04 music/sound settings <br>
{2 byte} function <br>
{data length byte} data <br>
{2 byte} checksum <br>

#### Receive (sound and timer, lamp has no response) <br> 
{4 byte} header [0x55, 0xaa] <br>
{2 byte} data length <br>
{2 byte} 0x88 lamp/effect, 0x85 timer, 0x84 music/sound settings <br>
{2 byte} function <br>
{data length byte} data <br>
{2 byte} checksum <br>






