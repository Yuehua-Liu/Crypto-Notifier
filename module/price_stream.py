import os
import asyncio
from binance import AsyncClient, BinanceSocketManager


class price_stream():
    """
    該物件用來做 Realtime 價格讀取，寫入 .txt 檔中，未來可以寫入資料庫
    一個 price_stream instance 專責處理一個報價
    所有 price_stream 由 price_stream_handler 來管理
    """

    def __init__(self, binance_manager, client, subscribed_symbol, frequency):
        # Binance Manager
        self.bm = binance_manager
        # AsyncClient Object
        self.client = client
        # 訂閱代號
        self.symbol = subscribed_symbol
        # 訂閱頻率
        self.freq = frequency
        # Task 狀態
        self.status = False

    # 接收報價
    async def subscribe_symbol(self):
        # client = await AsyncClient.create()
        # bm = BinanceSocketManager(client)

        # start any sockets here, i.e a trade socket
        ts = self.bm.kline_socket(self.symbol)

        # then start receiving messages
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                print(res)

                with open(f"./module/{self.symbol}_price.txt", "a+") as f:
                    f.writelines(str([res['E'], res['s'], res['k']]) + "\n")

        await self.client.close_connection()


# test code
if __name__ == "__main__":
    async def main():
        # sub_list = ['BTCUSDT', 'ETHUSDT', 'LINKUSDT']
        # for each in sub_list:
        #     if os.exists('.\{each}_price.txt'):
        #         pass
        #     else:
        #         os.file

        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        
        
        
        crypto_task1 = price_stream(bm, client, 'BTCUSDT', '1min')
        crypto_task2 = price_stream(bm, client, 'ETHUSDT', '1min')

        t1 = asyncio.create_task(crypto_task1.subscribe_symbol())
        t2 = asyncio.create_task(crypto_task2.subscribe_symbol())

        await t1
        await t2

        # t1 = asyncio.create_task(subscribe_symbol('BTCUSDT'))
        # t2 = asyncio.create_task(subscribe_symbol('ETHUSDT'))
        # t3 = asyncio.create_task(subscribe_symbol('LINKUSDT'))
        # await t1
        # await t2
        # await t3

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
