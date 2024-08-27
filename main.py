import requests
import time
from concurrent.futures import ThreadPoolExecutor


# 定义请求函数
def send_request(url, headers, rest, i):
    response = requests.get(url, headers=headers)

    # 检查是否有重定向
    if response.history:
        for resp in response.history:
            if resp.status_code == 302:
                print(f"请求 {i + 1} 被302到: {resp.headers['Location']}")

    # 检查请求是否成功
    if response.status_code == 200:
        print(f"\n请求 {i + 1} 成功，最终服务器地址: {response.url}\n")
        print('\n')
    else:
        print(f"请求 {i + 1} 失败，状态码: {response.status_code}\n")
        print('\n')

    # 每次请求后休息指定时间
    time.sleep(int(rest))


def main():
    url = input('请求地址：')
    num_requests = int(input('请求次数：'))
    ua = input('UA(不输入我就用默认的):')
    rest = input('请求间隔(单位：秒)(仅支持整数)：')
    workers = int(input('要多少线程(嘿嘿)：'))
    print('\n')

# 默认值(好屎山啊)
    if not ua:
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    if not num_requests:
        num_requests = 10
    if not rest:
        rest = 3
    if not workers:
        workers = 1

    headers = {"User-Agent": ua}

    # 使用 ThreadPoolExecutor 进行多线程请求
    with ThreadPoolExecutor(max_workers=workers) as executor:  # max_workers 可以根据需求调整
        futures = [executor.submit(send_request, url, headers, rest, i) for i in range(num_requests)]

        # 等待所有线程完成
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()