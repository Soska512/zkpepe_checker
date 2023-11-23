import pyuseragents, aiohttp, random, asyncio, time

headers = {
        'authority': 'www.zksyncpepe.com',
        'scheme': 'https',
        'cache-control': 'no-cache',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk-UA;q=0.6,uk;q=0.5', 
        'referer': 'https://www.zksyncpepe.com/airdrop',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': pyuseragents.random(),}


async def check(wallet, session):
    retries = 3
    delay = 5
    while retries > 0:
        try:
            url = f'https://www.zksyncpepe.com/resources/amounts/{wallet}.json'
            async with session.get(url) as response:
                if '[' in await response.text():
                    with open('results.txt', 'a') as f:
                        f.write(f'{wallet} got {await response.text()} $ZKPEPE\n')
                        break
                else:
                    with open('results.txt', 'a') as f:
                        f.write(f'{wallet} got 0 $ZKPEPE\n')
                    break
        except aiohttp.ClientError as e:
            print(f"Request failed for {wallet}. Retrying in {delay} seconds.")
            retries -= 1
            await asyncio.sleep(delay)
            delay *= random.uniform(1, 2)  # random delay here
            continue

async def main():
    print('''
  ______                                   __                 ______                           __                 
 /      \                                 /  |               /      \                         /  |                
/$$$$$$  |  ______   __    __   ______   _$$ |_     ______  /$$$$$$  | _____  ____    ______  $$ |____    ______  
$$ |  $$/  /      \ /  |  /  | /      \ / $$   |   /      \ $$ |__$$ |/     \/    \  /      \ $$      \  /      \ 
$$ |      /$$$$$$  |$$ |  $$ |/$$$$$$  |$$$$$$/   /$$$$$$  |$$    $$ |$$$$$$ $$$$  |/$$$$$$  |$$$$$$$  | $$$$$$  |
$$ |   __ $$ |  $$/ $$ |  $$ |$$ |  $$ |  $$ | __ $$ |  $$ |$$$$$$$$ |$$ | $$ | $$ |$$    $$ |$$ |  $$ | /    $$ |
$$ \__/  |$$ |      $$ \__$$ |$$ |__$$ |  $$ |/  |$$ \__$$ |$$ |  $$ |$$ | $$ | $$ |$$$$$$$$/ $$ |__$$ |/$$$$$$$ |
$$    $$/ $$ |      $$    $$ |$$    $$/   $$  $$/ $$    $$/ $$ |  $$ |$$ | $$ | $$ |$$       |$$    $$/ $$    $$ |
 $$$$$$/  $$/        $$$$$$$ |$$$$$$$/     $$$$/   $$$$$$/  $$/   $$/ $$/  $$/  $$/  $$$$$$$/ $$$$$$$/   $$$$$$$/ 
                    /  \__$$ |$$ |                                                                                
                    $$    $$/ $$ |                                                                                
                     $$$$$$/  $$/                                                                                 

          ''')
    wallets = []
    with open('wallets.txt', 'r') as file:
        wallets = file.readlines()
    
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [check(wallet.lower().strip(), session) for wallet in wallets]
        await asyncio.gather(*tasks)

start_time = time.time()
asyncio.run(main())
print(f"Execution time: {time.time() - start_time} seconds")