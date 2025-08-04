from selenium import webdriver  # Import the webdriver module
from selenium.webdriver.edge.service import Service # Import the Service class for Edge
from selenium.webdriver.edge.options import Options # Import Options for Edge browser
from selenium.webdriver.common.by import By  
import time
import os
from selenium.webdriver.support import expected_conditions as EC
import sys

def open_edge():

    # prepare

    download_dir = os.path.abspath("datesheet_downloads")
    os.makedirs(download_dir, exist_ok=True)
    # Create an instance of Options for Edge browser
    options = Options()  
    options.use_chromium = True  # 必须开启这个选项
    options.add_argument('--log-level=3')  # 只输出 fatal 错误，忽略 info 和 warning
    # keep alive / not auto exit when done
    options.add_experimental_option("detach", True) 
    options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "plugins.always_open_pdf_externally": True,  # 不直接在浏览器中打开 PDF
}) 
   
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    driver_path = os.path.join(base_path, 'msedgedriver.exe')
    service = Service(executable_path=driver_path)  
   
    edge = webdriver.Edge(service=service, options=options)  

    # start position and size 
    edge.set_window_position(100,200)
    edge.set_window_size(800,600)

    #implicitly wait time 
    edge.implicitly_wait(10)
    return edge


def edge_quit(edge:webdriver.Edge):
    edge.quit()



if __name__ == '__main__':

    edge = open_edge()
    
    def baidu_search():
      # step2 - open a webpage 
      # Open the specified URL in the Edge browser   
      edge.get('https://baidu.com')  
      # get search tag 
      searchBox = edge.find_element(by=By.ID,value='kw')
      # print(searchBox)
      time.sleep(2)
      # input the words we want 
      searchBox.send_keys('just a testing')
      time.sleep(2)
      # search button
      button = edge.find_element(by=By.ID,value='su')
      time.sleep(2)
      # click
      button.click()
      time.sleep(3)
      edge.quit()


    # open website of IFM
    edge.get('https://www.ifm.cn/cn/zh')


    def click_accept_all(edge, max_wait=10):
        for i in range(max_wait):
            try:
                found = edge.execute_script("""
                    const root = document.querySelector('#usercentrics-root');
                    if (!root) return false;
                    const shadow = root.shadowRoot;
                    if (!shadow) return false;
                    const btn = shadow.querySelector('button[data-testid="uc-accept-all-button"]');
                    if (btn) { btn.click(); return true; }
                    return false;
                """)
                if found:
                    print("✅ The accept all button was clicked successfully.")
                    return True
            except Exception as e:
                pass
            time.sleep(1)
        print("⚠️ The accept all button was not found.")
        return False
    
    click_accept_all(edge)
  
   
    
   
    # Step 1:  search box   & input content   'SA5000'
    input_text = input("please input the text you want to search: (example: SA5000) ")
    step = edge.find_element(by=By.XPATH,value='//*[@id="search-bar__input"]')
    step.send_keys(input_text)  # 输入内容到搜索框中
    
    # Step 2:  click search btn
    time.sleep(2)
    step = edge.find_element(by=By.XPATH,value='//*[@id="form-search-bar"]/button/span')
    step.click()
    
    # Step 3:  result, click on 'sa5000'
    time.sleep(2)
    step = edge.find_element(by=By.XPATH,value='//*[@id="product"]/div/div[2]/div/div/div[1]/div/a')
    step.click()
   
    # Step 4:  download btn , click
    time.sleep(2)
    step = edge.find_element(by=By.XPATH,value='//*[@id="details"]/div[1]/div[1]/div/a')  
    step.click() 

    # step 5: chick if downloading ok
    time.sleep(5)
    # download_dir = "C:\\Users\\YourUsername\\Downloads"
    # if any(filename.endswith(".pdf") for filename in os.listdir(download_dir)):
    #     print("✅ 下载完成")
    # else:
    #     print("⚠️ 下载未完成")

    # step 6: close browser
    edge_quit(edge)