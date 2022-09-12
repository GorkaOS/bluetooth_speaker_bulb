from typing import Callable
from mylight import const
from mylight.connection import Connection
from mylight.light import Light
from mylight.speaker import Speaker
from bleak.backends.device import BLEDevice


class Bulb():
    def __init__(self, ble_device: BLEDevice) -> None:
        self._connection = Connection(ble_device, timeout=20, retries=3)
        self._light = Light()
        self._speaker = Speaker()

    @property
    def available(self) -> bool:
        return self._connection.is_connected()

    def add_callback_on_state_changed(self, func: Callable[[], None]) -> None:
        """
        Register callbacks to be called when lamp state is received or bt disconnected
        """
        self._connection._state_callbacks.append(func)

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
            category=const.SetBulbCategory.light,
            function=const.GetLightFunction
        )

    async def get_speaker_info(self) -> list:
        return await self.receive(
            category=const.SetBulbCategory.speaker,
            function=const.GetSpeakerFunction
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
        if self._light.brightness == brightness:
            await self.turn_on(brightness=None, rgb_color=None)
        elif brightness == 0:
            await self.turn_off()
        return await self.send(self._light.set_brightness(brightness=brightness))

    async def set_color_rgb(self, rgb: list) -> bool:
        return await self.send(self._light.set_color_rgb(rgb=rgb))

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
        return [effect.name for effect in const.Effects]

    def get_speaker_effects(self) -> list:
        return [effect.name for effect in const.SpeakerEffect]