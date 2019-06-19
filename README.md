基于HTTP协议的异步logger的Handler。

作为
    aiologger: https://github.com/B2W-BIT/aiologger
扩展的组件。

使用aiohttp发送http请求。

**Example**

    import time
    import aiohttp
    import asyncio
    from aiologger import Logger
    from aiologger.formatters.base import Formatter
    
    
    async def main():
        logger = Logger(name='my-logger')
        formatter = Formatter("%(name)s - %(asctime)s - %(levelname)s")
        handler = AsyncHTTPHandler(url="http://localhost:8081/index", method="POST", formatter=formatter)
        logger.add_handler(handler)
    
        tasks = [
         logger.debug("debug at stdout"),
         logger.info("info at stdout"),
         logger.warning("warning at stderr"),
         logger.error("error at stderr"),
         logger.critical("critical at stderr")
        ]
        await asyncio.wait(tasks)
        await logger.shutdown()
    
    
    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
