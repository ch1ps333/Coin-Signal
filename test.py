import requests
import asyncio

# Прокси-сервер
proxies = {
    'http': 'http://23.95.164.200:80',
    'https': 'http://38.183.144.117:1111'
}

async def res():
    result = await requests.get('https://zapper.xyz/ru', proxies=proxies)
    print(result.status_code)

asyncio.run(res())
