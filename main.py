import requests
import time

url = input('请求地址：')
requset_time = input('请求次数：')
headers = {"User-Agent": input('UA:')}
rest = input('每次请求之后要休息多久(单位：秒):')
print('\n')

for i in range(int(requset_time)):
    response = requests.get(url, headers=headers)
    if response.history:
        for resp in response.history:
            if resp.status_code == 302:
                print(f"302 到: {resp.headers['Location']}\n")
    if response.status_code == 200:
        print(f"最终服务器地址: {response.url}\n")
        print('\n')
        time.sleep(int(rest))
    else:
        print(f"请求 {i+1} 失败，状态码: {response.status_code}")
        time.sleep(int(rest))
