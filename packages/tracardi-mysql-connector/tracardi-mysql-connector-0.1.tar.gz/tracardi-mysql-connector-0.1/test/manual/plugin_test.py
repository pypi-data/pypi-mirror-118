import asyncio

from tracardi_mysql_connector.plugin import MysqlConnectorAction

init = dict(
    dbname='mysql',
    user='root',
    password=None,
    host='localhost',
    port=3306,
    query="SELECT * FROM user LIMIT 1;"
)
payload = {}


async def main():
    plugin = await MysqlConnectorAction.build(**init)
    try:
        result = await plugin.run(payload)
    finally:
        await plugin.close()

    print(result)

asyncio.run(main())
