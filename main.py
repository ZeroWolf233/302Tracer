import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 定义请求函数
def send_request(url, headers, rest, i):
    try:
        response = requests.get(url, headers=headers, timeout=10)  # 增加超时设置，防止请求长时间挂起

        # 检查是否有重定向
        if response.history:
            for resp in response.history:
                if resp.status_code == 302:
                    print(f"请求 {i + 1} 被302重定向到: {resp.headers['Location']}")

        # 检查请求是否成功
        if response.status_code == 200:
            print(f"\n请求 {i + 1} 成功，最终服务器地址: {response.url}\n\n"+"-"*100+"\n")
        else:
            print(f"请求 {i + 1} 失败，状态码: {response.status_code}\n\n"+"-"*100+"\n")

    except requests.exceptions.RequestException as e:
        print(f"请求 {i + 1} 失败，发生异常: {e}\n\n"+"-"*100+"\n")

    # 每次请求后休息指定时间
    time.sleep(int(rest))

def get_valid_int_input(prompt, default):
    while True:
        user_input = input(prompt)
        if not user_input:
            return default
        try:
            return int(user_input)
        except ValueError:
            print("杂鱼杂鱼，是无效的输入呢~\n")

def main():
    url = input('请求地址：')
    num_requests = get_valid_int_input('请求次数(默认10次)：', 10)
    ua = input('UA(不输入我就用默认的):') or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    rest = get_valid_int_input('请求间隔(单位：秒)(仅支持整数)(默认3秒)：', 1)
    workers = get_valid_int_input('要多少线程(嘿嘿)(默认1个线程)：', 1)
    print('\n')

    headers = {"User-Agent": ua}

    # 使用 ThreadPoolExecutor 进行多线程请求
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(send_request, url, headers, rest, i) for i in range(num_requests)]

        # 等待所有线程完成
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()