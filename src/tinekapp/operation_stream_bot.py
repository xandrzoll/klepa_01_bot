import asyncio

import aiohttp

from src.tinekapp.messages import trade_message
from src.tinekapp.service import TinkoffService

from settings import TINKOFF_TOKEN, TINKOFF_WATCH_ACCOUNT


async def main():
    ts = TinkoffService(TINKOFF_TOKEN, 'my_test_service')
    accounts_info = ts.get_accounts()
    accounts = {}
    for account in accounts_info:
        accounts[account.id] = account.name + ' ⭐️' if account.id in ('2021716683', '2119610855') else account.name
        print(account.id, accounts[account.id], account.id in TINKOFF_WATCH_ACCOUNT)

    server_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
    async for trade in ts.trades_stream(['2022101695']):
        message = trade_message(trade, accounts.get(trade.account_id))
        post_data = {
            'data': [
                {'message': message, 'chat': [140618149]}
            ]
        }
        try:
            await server_session.post(
                url='https://klepa.site/post_message',
                headers={'X-Secret-Value': 'ljdvh@odsjuv087sc126xna0933kka!ncjhxc258'},
                json=post_data
            )
        except Exception as err:
            print(err)
        print(message)

    await server_session.close()


if __name__ == "__main__":
    asyncio.run(main())
