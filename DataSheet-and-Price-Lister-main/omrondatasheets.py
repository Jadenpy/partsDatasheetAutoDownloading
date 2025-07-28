import requests
from bs4 import BeautifulSoup

def search_omron_japan(model: str):
    base_url = "https://www.fa.omron.co.jp"
    search_url = f"{base_url}/search/?q={model}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 查找第一个搜索结果链接
    first_result = soup.find("div", class_="prodSearchListInner")
    if not first_result:
        print("未找到型号")
        return

    link_tag = first_result.find("a", href=True)
    if not link_tag:
        print("未找到产品详情链接")
        return

    detail_url = base_url + link_tag["href"]
    print(f"详情页链接: {detail_url}")

    # 再次请求详情页，查找PDF
    detail_resp = requests.get(detail_url, headers=headers)
    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")

    pdf_link = detail_soup.find("a", href=True, string=lambda text: text and "仕様書" in text)
    if pdf_link:
        pdf_url = base_url + pdf_link['href']
        print(f"PDF 下载链接: {pdf_url}")
    else:
        print("未找到 PDF")

# 示例
search_omron_japan("CJ1W-AD081-V1")
