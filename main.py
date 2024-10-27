import aiohttp
import asyncio
import time

# 定义请求函数
async def send_request(session, url, headers, i, rest):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                print(f"请求 {i + 1} 成功")
            else:
                print(f"请求 {i + 1} 失败，状态码: {response.status}")
    except Exception as e:
        print(f"请求 {i + 1} 失败，发生异常: {e}")
    # 每次请求后休息指定时间
    time.sleep(rest)

def get_valid_int_input(prompt, default):
    while True:
        user_input = input(prompt)
        if not user_input:
            return default
        try:
            return int(user_input)
        except ValueError:
            print("杂鱼杂鱼~是无效的输入呢~\n")

async def main():
    url = input('请求地址：')
    num_requests = get_valid_int_input('请求次数(默认10次)：', 10)
    ua = input('UA(不输入我就用默认的):') or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    rest = get_valid_int_input('请求间隔(单位：秒)(仅支持整数)(默认3秒)：', 3)
    workers = get_valid_int_input('要多少线程(默认1个线程)：', 1)

    headers = {"User-Agent": ua}

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url, headers, i) for i in range(num_requests)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
    input('运行完成,请查看上方的结果')
