from typing import Generator, List, Any, Type

from ubotadapter import UBotAdapter, InboundProcessor


class BotsManager:
    def __init__(self):
        self._bots = {}

    def __iter__(self) -> Generator[UBotAdapter, Any, None]:
        return (b for b in self.bots)

    def add(self, bot: UBotAdapter):
        name = bot.channel
        if name not in self._bots:
            self._bots[name] = bot
        else:
            raise KeyError(f'Bot with name "{name}" already exists in bots manager.')

    @property
    def bots(self) -> List[UBotAdapter]:
        return list(self._bots.values())

    def get_bot_by_name(self, name: str) -> UBotAdapter:
        pass

    def set_inbound_processor(self, inbound_processor: Type[InboundProcessor]):
        for bot in self.bots:
            bot.set_inbound_processor(inbound_processor)
