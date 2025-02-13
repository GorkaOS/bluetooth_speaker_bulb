import asyncio
from typing import Callable

# import connection
from bleak.backends.device import BLEDevice

from .connection import Connection
from .const import *
from .light import Light
from .speaker import Speaker


class Bulb():
    def __init__(self, ble_device: BLEDevice) -> None:
        self._connection = Connection(ble_device, timeout=20, retries=3)
        self._light = Light()
        self._speaker = Speaker()

    async def connect(self) -> bool:
        return await self._connection.connect()

    async def disconnect(self) -> bool:
        return await self._connection.disconnect()

    async def get_device_name(self) -> str:
        return await self._connection.get_device_name()

    async def send(self, msg: str) -> bool:
        return await self._connection.send_cmd(msg)

    async def receive(self, category: str, function: str) -> list:
        return await self._connection.get_category_info(
            category=category,
            functions=function
        )

    async def get_light_info(self) -> list:
        return await self.receive(
            category=SetBulbCategory.light,
            function=GetLightFunction
        )

    async def get_speaker_info(self) -> list:
        return await self.receive(
            category=SetBulbCategory.speaker,
            function=GetSpeakerFunction
        )

    async def update(self) -> None:
        await self.update_light()
        await self.update_speaker()

    async def update_light(self) -> None:
        self._light.update(raw_data=await self.get_light_info())

    async def update_speaker(self):
        self._speaker.update(raw_data=await self.get_speaker_info())

    async def turn_on(self, brightness: int = None, rgb_color: list = None) -> bool:
        if brightness is not None:
            return await self.set_brightness(brightness=brightness)
        if rgb_color is not None:
            return await self.set_rgb_color(rgb_color=rgb_color)
        return await self.send(self._light.turn_on())

    async def turn_off(self) -> bool:
        return await self.send(self._light.turn_off())

    async def set_brightness(self, brightness: int) -> bool:
        # if self._light.brightness == brightness:
        #     return await self.turn_on(brightness=None, rgb_color=None)
        # elif brightness == 0:
        #     return await self.turn_off()
        return await self.send(self._light.set_brightness(brightness=brightness))

    async def set_color_rgb(self, rgb: list) -> bool:
        result = await self.send(self._light.set_color_rgb(rgb=rgb))
        asyncio.sleep(0.7)
        return result and await self.send(self._light.set_brightness(self._light.brightness))

    async def set_white_intensity(self, intensity: int) -> bool:
        return await self.send(self._light.set_white_intensity(intensity=intensity))

    async def set_white(self) -> bool:
        return await self.send(self._light.set_white())

    async def set_effect(self, effect: str) -> bool:
        return await self.send(self._light.set_effect(effect=effect))

    async def set_volume(self, volume: int) -> bool:
        return await self.send(self._speaker.set_speaker_level(level=volume))

    async def set_speaker_effect(self, effect: str) -> bool:
        return await self.send(self._speaker.set_speaker_effect(effect=effect))

    async def set_frequency_level(self, frequency: str, level: int) -> bool:
        return await self.send(self._speaker.set_speaker_level(level=level, function=frequency))

    def get_light_effects(self) -> list:
        return [effect.name for effect in Effects]

    def get_speaker_effects(self) -> list:
        return [effect.name for effect in SpeakerEffect]
