from src.tinekapp.tinek_types import TTrade


def trade_message(trade: TTrade, account_name: str):
    change_portfolio_percent = round((trade.price * trade.quantity) / trade.portfolio_total_amount, 2) * 100

    msg_trade_type = 'Покупка' if trade.order_type == 1 else 'Продажа'
    msg_trade_type_point = '🟢' if trade.order_type == 1 else '🔴'
    msg_trade_symbol = '+' if trade.order_type == 1 else '-'
    ticker = trade.ticker
    href = f'<a href="https://www.tinkoff.ru/invest/stocks/{ticker}?utm_source=security_share">{ticker}</a>'
    price = trade.price
    trade_date = trade.order_created_at
    trade_portfolio_percent = round(trade.portfolio_trade_amount / trade.portfolio_total_amount, 2) * 100
    message = f'{msg_trade_type_point} #{ticker} {href}\n' \
              f'💴 <b>{price}</b> {msg_trade_symbol}{change_portfolio_percent}% ({trade_portfolio_percent}%)\n' \
              f'💰 {trade_date} счет {account_name}\n' \
              f'{msg_trade_type} '

    return message
