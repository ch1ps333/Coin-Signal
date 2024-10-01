import asyncio
from binance.client import Client
from handlers.bot_commands import send_notification
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from requests import get

client = Client()

notified_coins_5m = {}
notified_coins_15m = {}
notified_coins_45m = {}
notified_coins_60m = {}
notified_coins_135m = {}
notified_coins_240m = {}
notified_coins_540m = {}
notified_coins_1440m = {}

async def get_coins():
    while True:
        print('s')
        tickers = client.get_ticker()
        usdt_coins = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]
        usdt_coins.sort(key=lambda x: float(x['priceChangePercent']), reverse=True)

        remove_old_coins()

        for coin in usdt_coins:
            price_change_percent = float(coin['priceChangePercent'])
            symbol = coin['symbol']

            if abs(price_change_percent) >= 5:
                klines_5m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=5)
                klines_15m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=15)
                klines_45m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=9)
                klines_60m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=12)
                klines_135m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=9)
                klines_240m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_30MINUTE, limit=8)
                klines_540m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=9)
                klines_1440m = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=24)


                open_price_5m = float(klines_5m[0][1])
                close_price_5m = float(klines_5m[-1][4])
                percent_change_5m = round(((close_price_5m - open_price_5m) / open_price_5m) * 100, 2)
                if abs(percent_change_5m) >= 5:
                    high_price_5m = max([float(kline[2]) for kline in klines_5m]) 
                    low_price_5m = min([float(kline[3]) for kline in klines_5m])  
                    highest_percent5m = (high_price_5m - open_price_5m) / open_price_5m * 100
                    lowest_percent5m = (low_price_5m - open_price_5m) / open_price_5m * 100
                    if symbol not in notified_coins_5m:
                        await process_coin(coin, percent_change_5m, 0, highest_percent5m, lowest_percent5m, 5)
                        notified_coins_5m[symbol] = (datetime.now(), percent_change_5m)
                    else:
                        previous_change_time_5m, previous_change_5m = notified_coins_5m[symbol]
                        if abs(percent_change_5m - previous_change_5m) >= 1:
                            await process_coin(coin, percent_change_5m, previous_change_5m, highest_percent5m, lowest_percent5m, 5)
                            notified_coins_5m[symbol] = (datetime.now(), percent_change_5m)

                open_price_15m = float(klines_15m[0][1])
                close_price_15m = float(klines_15m[-1][4])
                percent_change_15m = round(((close_price_15m - open_price_15m) / open_price_15m) * 100, 2)
                if abs(percent_change_15m) >= 5:
                    high_price_15m = max([float(kline[2]) for kline in klines_15m]) 
                    low_price_15m = min([float(kline[3]) for kline in klines_15m])  
                    highest_percent15m = (high_price_15m - open_price_15m) / open_price_15m * 100
                    lowest_percent15m = (low_price_15m - open_price_15m) / open_price_15m * 100
                    if symbol not in notified_coins_15m:
                        await process_coin(coin, percent_change_15m, 0, highest_percent15m, lowest_percent15m, 15)
                        notified_coins_15m[symbol] = (datetime.now(), percent_change_15m)
                    else:
                        previous_change_time_15m, previous_change_15m = notified_coins_15m[symbol]
                        if abs(percent_change_15m - previous_change_15m) >= 1:
                            await process_coin(coin, percent_change_15m, previous_change_15m, highest_percent15m, lowest_percent15m, 15)
                            notified_coins_15m[symbol] = (datetime.now(), percent_change_15m)

                open_price_45m = float(klines_45m[0][1])
                close_price_45m = float(klines_45m[-1][4])
                percent_change_45m = round(((close_price_45m - open_price_45m) / open_price_45m) * 100, 2)
                if abs(percent_change_45m) >= 5:
                    high_price_45m = max([float(kline[2]) for kline in klines_45m]) 
                    low_price_45m = min([float(kline[3]) for kline in klines_45m])  
                    highest_percent45m = (high_price_45m - open_price_45m) / open_price_45m * 100
                    lowest_percent45m = (low_price_45m - open_price_45m) / open_price_45m * 100
                    if symbol not in notified_coins_45m:
                        await process_coin(coin, percent_change_45m, 0, highest_percent45m, lowest_percent45m, 45)
                        notified_coins_45m[symbol] = (datetime.now(), percent_change_45m)
                    else:
                        previous_change_time_45m, previous_change_45m = notified_coins_45m[symbol]
                        if abs(percent_change_45m - previous_change_45m) >= 1:
                            await process_coin(coin, percent_change_45m, previous_change_45m, highest_percent45m, lowest_percent45m, 45)
                            notified_coins_45m[symbol] = (datetime.now(), percent_change_45m)

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
                        if abs(percent_change_60m - previous_change_60m) >= 1:
                            await process_coin(coin, percent_change_60m, previous_change_60m, highest_percent60m, lowest_percent60m, 60)
                            notified_coins_60m[symbol] = (datetime.now(), percent_change_60m)

                open_price_135m = float(klines_135m[0][1])
                close_price_135m = float(klines_135m[-1][4])
                percent_change_135m = round(((close_price_135m - open_price_135m) / open_price_135m) * 100, 2)
                if abs(percent_change_135m) >= 5:
                    high_price_135m = max([float(kline[2]) for kline in klines_135m]) 
                    low_price_135m = min([float(kline[3]) for kline in klines_135m])  
                    highest_percent135m = (high_price_135m - open_price_135m) / open_price_135m * 100
                    lowest_percent135m = (low_price_135m - open_price_135m) / open_price_135m * 100
                    if symbol not in notified_coins_135m:
                        await process_coin(coin, percent_change_135m, 0, highest_percent135m, lowest_percent135m, 135)
                        notified_coins_135m[symbol] = (datetime.now(), percent_change_135m)
                    else:
                        previous_change_time_135m, previous_change_135m = notified_coins_135m[symbol]
                        if abs(percent_change_135m - previous_change_135m) >= 1:
                            await process_coin(coin, percent_change_135m, previous_change_135m, highest_percent135m, lowest_percent135m, 135)
                            notified_coins_135m[symbol] = (datetime.now(), percent_change_135m)

                open_price_240m = float(klines_240m[0][1])
                close_price_240m = float(klines_240m[-1][4])
                percent_change_240m = round(((close_price_240m - open_price_240m) / open_price_240m) * 100, 2)
                if abs(percent_change_240m) >= 5:
                    high_price_240m = max([float(kline[2]) for kline in klines_240m]) 
                    low_price_240m = min([float(kline[3]) for kline in klines_240m])  
                    highest_percent240m = (high_price_240m - open_price_240m) / open_price_240m * 100
                    lowest_percent240m = (low_price_240m - open_price_240m) / open_price_240m * 100
                    if symbol not in notified_coins_240m:
                        await process_coin(coin, percent_change_240m, 0, highest_percent240m, lowest_percent240m, 240)
                        notified_coins_240m[symbol] = (datetime.now(), percent_change_240m)
                    else:
                        previous_change_time_240m, previous_change_240m = notified_coins_240m[symbol]
                        if abs(percent_change_240m - previous_change_240m) >= 1:
                            await process_coin(coin, percent_change_240m, previous_change_240m, highest_percent240m, lowest_percent240m, 240)
                            notified_coins_240m[symbol] = (datetime.now(), percent_change_240m)

                open_price_540m = float(klines_540m[0][1])
                close_price_540m = float(klines_540m[-1][4])
                percent_change_540m = round(((close_price_540m - open_price_540m) / open_price_540m) * 100, 2)
                if abs(percent_change_540m) >= 5:
                    high_price_540m = max([float(kline[2]) for kline in klines_540m]) 
                    low_price_540m = min([float(kline[3]) for kline in klines_540m])  
                    highest_percent540m = (high_price_540m - open_price_540m) / open_price_540m * 100
                    lowest_percent540m = (low_price_540m - open_price_540m) / open_price_540m * 100
                    if symbol not in notified_coins_540m:
                        await process_coin(coin, percent_change_540m, 0, highest_percent540m, lowest_percent540m, 540)
                        notified_coins_540m[symbol] = (datetime.now(), percent_change_540m)
                    else:
                        previous_change_time_540m, previous_change_540m = notified_coins_540m[symbol]
                        if abs(percent_change_540m - previous_change_540m) >= 1:
                            await process_coin(coin, percent_change_540m, previous_change_540m, highest_percent540m, lowest_percent540m, 540)
                            notified_coins_540m[symbol] = (datetime.now(), percent_change_540m)

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
                        if abs(percent_change_1440m - previous_change_1440m) >= 1:
                            await process_coin(coin, percent_change_1440m, previous_change_1440m, highest_percent1440m, lowest_percent1440m, 1440)
                            notified_coins_1440m[symbol] = (datetime.now(), percent_change_1440m)
                  


def remove_old_coins():
    now = datetime.now()
    two_days_ago = now - timedelta(days=2)
    
    all_notified_coins = {**notified_coins_5m, **notified_coins_15m, **notified_coins_45m,
                          **notified_coins_60m, **notified_coins_135m, **notified_coins_240m,
                          **notified_coins_540m, **notified_coins_1440m}

    keys_to_remove = [symbol for symbol, (timestamp, _) in all_notified_coins.items() if timestamp < two_days_ago]

    for key in keys_to_remove:
        if key in notified_coins_5m:
            del notified_coins_5m[key]
        if key in notified_coins_15m:
            del notified_coins_15m[key]
        if key in notified_coins_45m:
            del notified_coins_45m[key]
        if key in notified_coins_60m:
            del notified_coins_60m[key]
        if key in notified_coins_135m:
            del notified_coins_135m[key]
        if key in notified_coins_240m:
            del notified_coins_240m[key]
        if key in notified_coins_540m:
            del notified_coins_540m[key]
        if key in notified_coins_1440m:
            del notified_coins_1440m[key]


async def process_coin(coin, price_change_percent, previous_change, highest_percent, lowest_percent, minute_analysis):
    current_price = coin['lastPrice']
    symbol_clean = coin['symbol'].replace('USDT', '')
    url = f"https://www.binance.com/en/trade/{symbol_clean}_USDT"
    res = get(url)
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
            previous_change, price_change_percent, url, minute_analysis
        )

def run_get_coins():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_coins())

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(5):
            executor.submit(run_get_coins)