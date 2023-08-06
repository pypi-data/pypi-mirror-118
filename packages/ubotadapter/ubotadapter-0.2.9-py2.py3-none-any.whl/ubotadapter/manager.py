from typing import Generator, List, Any, Type

from ubotadapter import UBotAdapter, InboundProcessor


class BotsManager:
    def __init__(self):
        self._bots = {}

    def __iter__(self) -> Generator[UBotAdapter, Any, None]:
        return (b for b in self.bots)

    def __getitem__(self, bot_name: str) -> UBotAdapter:
        return self.get_bot_by_name(bot_name)

    def add(self, bot: UBotAdapter):
        name = bot.info.name
        if name not in self._bots:
            self._bots[name] = bot
        else:
            raise KeyError(f'Bot with name "{name}" already exists in bots manager.')

    @property
    def bots(self) -> List[UBotAdapter]:
        return list(self._bots.values())

    def get_bot_by_name(self, bot_name: str) -> UBotAdapter:
        return self._bots[bot_name]

    def set_inbound_processor(self, inbound_processor: Type[InboundProcessor]):
        for bot in self.bots:
            bot.set_inbound_processor(inbound_processor)
