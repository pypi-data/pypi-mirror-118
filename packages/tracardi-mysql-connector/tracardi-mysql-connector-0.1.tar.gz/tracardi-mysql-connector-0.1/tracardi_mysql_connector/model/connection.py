import asyncio
import aiomysql
from pydantic import BaseModel


class Connection(BaseModel):
    dbname: str
    user: str
    password: str = None
    host: str
    port: int = 3306
    query: str = "SELECT 1"

    async def connect(self):
        loop = asyncio.get_event_loop()
        return await aiomysql.create_pool(host=self.host, port=self.port,
                                          user=self.user, password=self.password,
                                          db=self.dbname, loop=loop)
