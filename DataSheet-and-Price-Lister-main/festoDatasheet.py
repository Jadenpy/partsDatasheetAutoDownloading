import requests
from time import sleep


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'TE': 'trailers',
    'Cookie': 'LastSite=cn-zh-001; JHYSESSIONID=Y0-0cf93282-9b56-4c98-9a4c-ef74ec9d4154.accstorefront-b6779c966-prqqd; ROUTE=.accstorefront-b6779c966-prqqd'  # Replace with your actual cookie if needed

}

# session = requests.Session() #Create a session to persist certain parameters across requests

# base URL for Festo datasheets
base_url = "https://www.festo.com.cn/cn/zh/a/download-document/datasheet/"

# the spare part serial number
sn = "8130716"
# print(f'{sn}的datasheet地址为：',base_url + sn)


# resp = session.get(f"{base_url}{sn}")
resp = requests.get(f"{base_url}{sn}",headers=headers)  # Send a GET request to the URL with the specified headers

res_type = resp.headers.get('Content-Type')  # Get the content type of the response

print('响应类型:', res_type)  # Print the content type of the response



# Check if the response includes a PDF file

if 'application/pdf' in res_type:
    print(f"正在下载 {sn} 的数据表...")
    with open(f"{sn}.pdf", 'wb') as f:
        f.write(resp.content)  # Write the content of the response to a PDF file
        print(f'{sn}的数据表已下载成功！')
else:
    print(resp.text[:500])  # Print the first 1000 characters of the response text for debugging
    print(f"未找到 {sn} 的数据表,可能被重定向到 HTML 页面或遭遇403。")
