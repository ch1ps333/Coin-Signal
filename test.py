import asyncio
from binance.client import Client
from handlers.bot_commands import send_notification
from datetime import datetime, timedelta


client = Client()

notified_coins = {}

async def get_coins():
    while True:
        tickers = client.get_ticker()  # Удалите await здесь
        usdt_coins = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]
        usdt_coins.sort(key=lambda x: float(x['priceChangePercent']), reverse=True)

        for coin in usdt_coins:
            price_change_percent = float(coin['priceChangePercent'])
            symbol = coin['symbol']

            klines_5m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=5)
            klines_15m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=15)
            klines_45m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=9)
            klines_60m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=12)
            klines_135m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=9)
            klines_240m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_30MINUTE, limit=8)
            klines_540m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=9)
            klines_1440m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=24)

            # Проверка на наличие данных
            if not (klines_5m and klines_15m and klines_45m and klines_60m and klines_135m and klines_240m and klines_540m and klines_1440m):
                continue

            open_price_5m = float(klines_5m[0][1])
            close_price_5m = float(klines_5m[-1][4])
            percent_change_5m = ((close_price_5m - open_price_5m) / open_price_5m) * 100

            open_price_15m = float(klines_15m[0][1])
            close_price_15m = float(klines_15m[-1][4])
            percent_change_15m = ((close_price_15m - open_price_15m) / open_price_15m) * 100

            open_price_45m = float(klines_45m[0][1])
            close_price_45m = float(klines_45m[-1][4])
            percent_change_45m = ((close_price_45m - open_price_45m) / open_price_45m) * 100

            open_price_60m = float(klines_60m[0][1])
            close_price_60m = float(klines_60m[-1][4])
            percent_change_60m = ((close_price_60m - open_price_60m) / open_price_60m) * 100

            open_price_135m = float(klines_135m[0][1])
            close_price_135m = float(klines_135m[-1][4])
            percent_change_135m = ((close_price_135m - open_price_135m) / open_price_135m) * 100

            open_price_240m = float(klines_240m[0][1])
            close_price_240m = float(klines_240m[-1][4])
            percent_change_240m = ((close_price_240m - open_price_240m) / open_price_240m) * 100

            open_price_540m = float(klines_540m[0][1])
            close_price_540m = float(klines_540m[-1][4])
            percent_change_540m = ((close_price_540m - open_price_540m) / open_price_540m) * 100

            open_price_1440m = float(klines_1440m[0][1])
            close_price_1440m = float(klines_1440m[-1][4])
            percent_change_1440m = ((close_price_1440m - open_price_1440m) / open_price_1440m) * 100
            current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])

            # Получаем свечи за последние 24 часа (24 свечи с интервалом 1 час)
            klines_1440m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=24)

            # Цена открытия 24 часа назад
            open_price_1440m = float(klines_1440m[0][1])

            # Рассчитываем изменение процента на основе текущей цены
            percent_change_1440m = ((current_price - open_price_1440m) / open_price_1440m) * 100

            # Вывод результатов
            print(f"Процент изменения за 5 минут: {percent_change_5m:.2f}%")
            print(f"Процент изменения за 15 минут: {percent_change_15m:.2f}%")
            print(f"Процент изменения за 45 минут: {percent_change_45m:.2f}%")
            print(f"Процент изменения за 60 минут: {percent_change_60m:.2f}%")
            print(f"Процент изменения за 135 минут: {percent_change_135m:.2f}%")
            print(f"Процент изменения за 240 минут: {percent_change_240m:.2f}%")
            print(f"Процент изменения за 540 минут: {percent_change_540m:.2f}%")
            print(f"Процент изменения за 3600 минут: {percent_change_1440m:.2f}%")
            print(price_change_percent)
            symbol_clean = coin['symbol'].replace('USDT', '')
            url = f"https://www.binance.com/en/trade/{symbol_clean}_USDT"
            print(url)

        # Задержка между итерациями
        await asyncio.sleep(60)  # Задержка в 60 секунд

# Запуск корутины
asyncio.run(get_coins())
