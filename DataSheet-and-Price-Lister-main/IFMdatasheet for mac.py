from selenium import webdriver  # Import the webdriver module
from selenium.webdriver.edge.service import Service # Import the Service class for Edge
from selenium.webdriver.edge.options import Options # Import Options for Edge browser
# import BY
from selenium.webdriver.common.by import By  
import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def open_edge():

    # prepare

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)
    # Create an instance of Options for Edge browser
    options = Options()  
    options.use_chromium = True  # 必须开启这个选项
    # keep alive / not auto exit when done
    options.add_experimental_option("detach", True) 
    options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "plugins.always_open_pdf_externally": True,  # 不直接在浏览器中打开 PDF
}) 
    # disable sandbox model
    # options.add_argument('--no-sandbox')
    
    # create a service object
    # Specify the path to the Edge WebDriver executable
    service = Service(executable_path='/Users/jaden/Library/CloudStorage/OneDrive-个人/桌面/code/partsDatasheetAutoDownloading/edgedriver_mac64_m1/msedgedriver')  

    # step1 - create a webdriver object
    # Create a WebDriver instance for Edge browser
    edge = webdriver.Edge(service=service, options=options)  

    # start position and size 
    edge.set_window_position(100,200)
    edge.set_window_size(800,600)

    #implicitly wait time 
    edge.implicitly_wait(10)
    
    

    return edge


# step4 - input something in the search box
# I think that need to wait the page to load before finding elements
  # Wait for 10 seconds for the page to load before finding elements
"""
search_box = edge.find_element("id", "kw")  # Find the search box element by its ID
# any methods to find element: find_element_by_id, find_element_by_name, find_element_by_xpath, find_element_by_css_selector
search_box.send_keys("Selenium")  # Input the text "Selenium" into the search box

# step5 - submit the form  enter key
search_box.submit()  # Submit the search form by pressing Enter

"""

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

    def open_IFM():
        # open website of IFM
        edge.get('https://www.ifm.cn/cn/zh')

        # time.sleep(5)
        # # window handles
        # handles = edge.window_handles
        # print(f'所有的句柄：{handles}')

        try:
            # # 等待最多 10 秒直到“接受所有”按钮出现
            # accept_button = WebDriverWait(edge, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="uc-center-container"]/div[2]/div/div[1]/div/button[3]'))
            # )
            # accept_button.click()
            
            
            
            
            wait = WebDriverWait(edge, 10)

            # 等待并点击“全部接受”按钮
            accept_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="uc-accept-all-button"]'))
            )
            accept_button.click()
            
            print("✅ 已点击隐私弹窗中的“接受所有”按钮")

        except:
            print("⚠️ 未检测到隐私弹窗，可能已经被接受或未出现")
            
            
        

        # html_source = edge.page_source
        # print(html_source)

        """
        # Step 1:  search box   & input content   'SA5000'
        
        step = edge.find_element(by=By.XPATH,value='//*[@id="search-bar__input"]')
        step.send_keys('SA5000')
       
        # Step 2:  click search btn
        step = edge.find_element(by=By.XPATH,value='//*[@id="form-search-bar"]/button/span')
        step.click()

        # Step 3:  result, click on 'sa5000'
        step = edge.find_element(by=By.XPATH,value='//*[@id="product"]/div/div[2]/div/div/div[1]/div/a')
        step.click()
        # Step 4:  download btn , click
        step = edge.find_element(by=By.XPATH,value='//*[@id="details"]/div[1]/div[1]/div/a')  
        step.click()   
        # accept_btn = edge.find_element(By.XPATH,'/html/body/div[8]//div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/button[3]')
        # print(f'全部同意按钮：{accept_btn}')

        """

    open_IFM()
    # baidu_search()