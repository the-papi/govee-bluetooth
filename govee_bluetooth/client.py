import asyncio
import uuid

from bleak import BleakClient, BLEDevice

from govee_bluetooth.proto import GoveePower, GoveeProtocol


class GoveeClient:

    def __init__(
            self,
            client: BleakClient,
            proto: GoveeProtocol,
            service: uuid.UUID = uuid.UUID("00010203-0405-0607-0809-0a0b0c0d2b11"),
    ):
        self.client = client
        self.proto = proto
        self.service = service
        self._keep_alive_loop_running = False

    async def send_keep_alive(self):
        await self.client.write_gatt_char(self.service, self.proto.keep_alive(), True)

    async def keep_alive_loop(self):
        self._keep_alive_loop_running = True
        while self._keep_alive_loop_running:
            await self.send_keep_alive()
            await asyncio.sleep(2)

    async def stop_keep_alive_loop(self):
        self._keep_alive_loop_running = False

    async def set_power(self, power: GoveePower):
        await self.client.write_gatt_char(self.service, self.proto.power(power), True)

    async def set_rgb(self, segments: int, red: int, green: int, blue: int):
        await self.client.write_gatt_char(self.service, self.proto.rgb(segments, red, green, blue), True)

    async def set_brightness(self, segments: int, brightness: int):
        await self.client.write_gatt_char(self.service, self.proto.brightness(segments, brightness), True)
