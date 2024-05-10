import datetime
from dataclasses import dataclass
from decimal import Decimal

from tinkoff.invest import Quotation, MoneyValue
from tinkoff.invest.utils import now, quotation_to_decimal


class TType:
    @classmethod
    def from_object(cls, obj):
        values = []

        for k, v in cls.__dataclass_fields__.items():
            values.append(getattr(obj, k))

        return cls(*values)

@dataclass
class TAccount(TType):
    id: int
    name: str
    opened_date: datetime.datetime
    closed_date: datetime.datetime

@dataclass
class TValue:
    units: int
    nano: int

@dataclass
class TTrade:
    order_id: int
    account_id: int
    figi: str
    order_created_at: str
    order_type: int
    trades_count: int
    price: float
    quantity: int
    ticker: str = ''
    portfolio_total_amount: Decimal = 0
    portfolio_trade_amount: Decimal = 0

    @classmethod
    def from_object(cls, obj):
        order_id = getattr(obj, 'order_id')
        account_id = getattr(obj, 'account_id')
        figi = getattr(obj, 'figi')
        order_created_at = getattr(obj, 'created_at')
        order_created_at = order_created_at.astimezone().strftime('%d.%m %H:%M:%S')
        order_type = getattr(obj, 'direction')
        order_type = 1 if order_type == 1 else -1

        trades = getattr(obj, 'trades')
        trades_count = 1
        price = 0
        sum_price_volume = 0
        sum_quantity = 0
        for trade in trades:
            trades_count += 1
            quantity = trade.quantity
            price += quotation_to_decimal(trade.price)
            sum_price_volume += price * quantity
            sum_quantity += quantity
        price = round(sum_price_volume / sum_quantity, 4)
        return cls(order_id, account_id, figi, order_created_at, order_type, trades_count, price, sum_quantity)
