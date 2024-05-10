from tinkoff.invest import Client, AsyncClient, InstrumentIdType
from tinkoff.invest.async_services import AsyncServices
from tinkoff.invest.retrying.aio.client import AsyncRetryingClient
from tinkoff.invest.retrying.settings import RetryClientSettings
from tinkoff.invest.utils import quotation_to_decimal

from src.tinekapp.tinek_types import TAccount, TTrade


class TinkoffService:
    retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)

    def __init__(self, token: str, app_name: str = ''):
        self._token = token
        self._app_name = app_name

    def get_accounts(self):
        with Client(self._token) as client:
            accounts = client.users.get_accounts()
        accounts = [TAccount.from_object(acc) for acc in accounts.accounts]
        return accounts

    async def trades_stream(self, accounts: list):
        async with AsyncRetryingClient(self._token, settings=self.retry_settings) as client:
            async for trade in client.orders_stream.trades_stream(accounts=accounts):
                if not trade.order_trades:
                    continue
                trade_info = TTrade.from_object(trade.order_trades)
                instrument = await self.instrument_by_figi(trade_info.figi, client)
                portfolio = await self.portfolio(trade_info.account_id, client)
                portfolio_trade_amount = 0

                for pos in portfolio.positions:
                    if pos.figi == trade_info.figi:
                        portfolio_trade_amount = quotation_to_decimal(pos.quantity) * quotation_to_decimal(pos.average_position_price_pt)
                        break

                trade_info.ticker = instrument.instrument.ticker
                trade_info.portfolio_total_amount = quotation_to_decimal(portfolio.total_amount_portfolio)
                trade_info.portfolio_trade_amount = portfolio_trade_amount

                yield trade_info

    async def portfolio(self, account_id: str, client: AsyncServices = None):
        if client:
            data = await client.operations.get_portfolio(account_id=account_id)
        else:
            async with AsyncClient(self._token) as client:
                data = await client.operations.get_portfolio(account_id=account_id)
        return data

    async def instrument_by_figi(self, figi, client: AsyncServices = None):
        if client:
            data = await client.instruments.get_instrument_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        else:
            async with AsyncClient(self._token) as client:
                data = await client.instruments.get_instrument_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        return data
