import re
import aiohttp
from yarl import URL
from typing import Union, Optional, Dict
from asyncio import AbstractEventLoop
from aiologger.levels import LogLevel
from aiologger.formatters.base import Formatter
from aiologger.filters import Filter
from aiologger.handlers.base import Handler
from aiologger.records import LogRecord

StrOrURL = Union[str, URL]


def _get_msg_dict(self, record: LogRecord) -> Dict[str, str]:
    """
    :param self:
    :param record:
    :return:
    """
    record.message = record.get_message()
    record.asctime = self.format_time(record, self.datefmt)
    params = re.findall("%\((.*?)\)", self._fmt)
    _d = {}
    for i in params:
        _v = record.__dict__.get(i)
        if isinstance(_v, LogLevel):
            _v = _v.value
        _d[i] = str(_v) if _v else ''
    return _d


class AsyncHTTPHandler(Handler):

    def __init__(self,
                 url: StrOrURL,
                 method: str="GET",
                 level: Union[str, int, LogLevel] = LogLevel.NOTSET,
                 formatter: Formatter = None,
                 filter: Filter = None,
                 *,
                 loop: Optional[AbstractEventLoop] = None,
                 ):
        super().__init__(loop=loop)
        self._url = url
        self._method = method.upper()
        self.level = level
        self.formatter: Formatter = formatter if formatter else Formatter()
        self.formatter.__class__.get_msg_dict = _get_msg_dict
        # self.formatter.get_msg_dict = _get_msg_dict  # add get_msg_dict for formatter
        if filter:
            self.add_filter(filter)

    @property
    def initialized(self):
        return True

    async def emit(self, record: LogRecord):
        func = getattr(self.formatter, "get_msg_dict")
        data = func(record)
        kwargs = {
            "url": self._url,
            "method": self._method
        }
        if self._method == "POST":
            kwargs["data"] = data
        else:
            kwargs["params"] = data

        async with aiohttp.request(**kwargs):
            pass

    async def close(self):
        pass
