import asyncpg
from pydantic.main import BaseModel


class Connection(BaseModel):
    dbname: str
    user: str
    password: str
    host: str = 'localhost'
    port: int = 5439

    async def connect(self) -> asyncpg.connection.Connection:
        return await asyncpg.connect(database=self.dbname,
                                     user=self.user,
                                     password=self.password,
                                     host=self.host,
                                     port=self.port)
