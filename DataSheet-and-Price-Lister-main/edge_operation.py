from selenium import webdriver  # Import the webdriver module
from selenium.webdriver.edge.service import Service # Import the Service class for Edge
from selenium.webdriver.edge.options import Options # Import Options for Edge browser
from selenium.webdriver.common.by import By  
# import time
import os
# from selenium.webdriver.support import expected_conditions as EC
import sys

def open_edge(implicitly_wait=10):

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
    edge.set_window_position(5,5)
    edge.set_window_size(1200,600)

    #implicitly wait time 
    edge.implicitly_wait(10)
    return edge


def edge_quit(edge:webdriver.Edge):
    edge.quit()

