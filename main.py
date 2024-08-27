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
    url = input('请输入请求地址：')
    num_requests = int(input('请输入请求次数：'))
    headers = {"User-Agent": input('请输入UA：')}
    rest = input('每次请求之后休息多久(单位：秒)(仅支持整数)：')
    workers = int(input('要多少线程(嘿嘿)：'))
    print('\n')

    # 使用 ThreadPoolExecutor 进行多线程请求
    with ThreadPoolExecutor(max_workers=workers) as executor:  # max_workers 可以根据需求调整
        futures = [executor.submit(send_request, url, headers, rest, i) for i in range(num_requests)]

        # 等待所有线程完成
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()