import asyncio
from binance.client import Client
from handlers.bot_commands import send_notification
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from requests import get

client = Client()

notified_coins_60m = {}
notified_coins_1440m = {}
counter = 0

async def get_coins():
    while True:
        global counter
        counter += 1
        print(counter)
        try:
            tickers = client.get_ticker()
        except Exception as err:
            print(err)
        usdt_coins = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]
        usdt_coins.sort(key=lambda x: float(x['priceChangePercent']), reverse=True)

        if counter > 500:
            remove_old_coins()

        for coin in usdt_coins:
            price_change_percent = float(coin['priceChangePercent'])
            symbol = coin['symbol']

            if abs(price_change_percent) >= 5:
                try:
                    klines_60m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=12)
                    klines_1440m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=24)
                except Exception as err:
                    print(err)


                if klines_60m:
                    open_price_60m = float(klines_60m[0][1])
                    close_price_60m = float(klines_60m[-1][4])
                    percent_change_60m = round(((close_price_60m - open_price_60m) / open_price_60m) * 100, 2)
                    if abs(percent_change_60m) >= 5:
                        high_price_60m = max([float(kline[2]) for kline in klines_60m]) 
                        low_price_60m = min([float(kline[3]) for kline in klines_60m])  
                        highest_percent60m = (high_price_60m - open_price_60m) / open_price_60m * 100
                        lowest_percent60m = (low_price_60m - open_price_60m) / open_price_60m * 100
                        if symbol not in notified_coins_60m:
                            await process_coin(coin, percent_change_60m, 0, highest_percent60m, lowest_percent60m, 60)
                            notified_coins_60m[symbol] = (datetime.now(), percent_change_60m)
                        else:
                            previous_change_time_60m, previous_change_60m = notified_coins_60m[symbol]
                            if abs(percent_change_60m - previous_change_60m) >= 5:
                                await process_coin(coin, percent_change_60m, previous_change_60m, highest_percent60m, lowest_percent60m, 60)
                                notified_coins_60m[symbol] = (datetime.now(), percent_change_60m)


                if klines_1440m:
                    open_price_1440m = float(klines_1440m[0][1])
                    close_price_1440m = float(klines_1440m[-1][4])
                    percent_change_1440m = round(price_change_percent, 2)
                    if abs(percent_change_1440m) >= 5:
                        high_price_1440m = max([float(kline[2]) for kline in klines_1440m]) 
                        low_price_1440m = min([float(kline[3]) for kline in klines_1440m])  
                        highest_percent1440m = (high_price_1440m - open_price_1440m) / open_price_1440m * 100
                        lowest_percent1440m = (low_price_1440m - open_price_1440m) / open_price_1440m * 100
                        if symbol not in notified_coins_1440m:
                            await process_coin(coin, percent_change_1440m, 0, highest_percent1440m, lowest_percent1440m, 1440)
                            notified_coins_1440m[symbol] = (datetime.now(), percent_change_1440m)
                        else:
                            previous_change_time_1440m, previous_change_1440m = notified_coins_1440m[symbol]
                            if abs(percent_change_1440m - previous_change_1440m) >= 5:
                                await process_coin(coin, percent_change_1440m, previous_change_1440m, highest_percent1440m, lowest_percent1440m, 1440)
                                notified_coins_1440m[symbol] = (datetime.now(), percent_change_1440m)
        await asyncio.sleep(60)


def remove_old_coins():
    now = datetime.now()
    two_days_ago = now - timedelta(days=2)
    
    all_notified_coins = {**notified_coins_60m, **notified_coins_1440m}

    keys_to_remove = [symbol for symbol, (timestamp, _) in all_notified_coins.items() if timestamp < two_days_ago]

    for key in keys_to_remove:
        if key in notified_coins_60m:
            del notified_coins_60m[key]
        if key in notified_coins_1440m:
            del notified_coins_1440m[key]


async def process_coin(coin, price_change_percent, previous_change, highest_percent, lowest_percent, minute_analysis):
    current_price = coin['lastPrice']
    symbol_clean = coin['symbol'].replace('USDT', '')
    url = f"https://www.binance.com/en/trade/{symbol_clean}_USDT"
    try:
        res = get(url)
    except Exception as err:
        print(err)
    if res.ok:
        if price_change_percent > previous_change and previous_change != 0:
            header_ukr = f"- {coin['symbol']}: {price_change_percent}% РІСТ\n"
            header_en = f"- {coin['symbol']}: {price_change_percent}% GROWTH\n"
            f"- {coin['symbol']}: {price_change_percent}% (Current rise/fall)\n"
        elif price_change_percent < previous_change and previous_change != 0:
            header_ukr = f"- {coin['symbol']}: {price_change_percent}% ПАДІННЯ\n"
            header_en = f"- {coin['symbol']}: {price_change_percent}% FALL\n"
        elif previous_change == 0:
            if price_change_percent > 0:
                header_ukr = f"- {coin['symbol']}: {price_change_percent}% РІСТ\n"
                header_en = f"- {coin['symbol']}: {price_change_percent}% GROWTH\n"
            elif price_change_percent < 0:
                header_ukr = f"- {coin['symbol']}: {price_change_percent}% ПАДІННЯ\n"
                header_en = f"- {coin['symbol']}: {price_change_percent}% FALL\n"   
        await send_notification(
            f"* Аналіз за {minute_analysis} хвилин *\n"
            f"{header_ukr}"
            f"- Поточна ціна: {current_price} USDT\n"
            f"- Максимальний зріст за 24 години: {highest_percent:.2f}%\n"
            f"- Максимальне падіння за 24 години: {lowest_percent:.2f}%\n",

            f"* Analysis in {minute_analysis} minutes *\n"
            f"{header_en}"
            f"- Current price: {current_price} USDT\n"
            f"- Maximum growth in 24 hours: {highest_percent:.2f}%\n"
            f"- Maximum drop in 24 hours: {lowest_percent:.2f}%\n",
            previous_change, price_change_percent, url, minute_analysis, coin['symbol']
        )

asyncio.run(get_coins())
