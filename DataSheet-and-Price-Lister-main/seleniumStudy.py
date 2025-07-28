from selenium import webdriver
from selenium.webdriver.edge.service import Service  # Import the Service class for Edge
from selenium.webdriver.edge.options import Options  # Import the Options class for Edge
from selenium.webdriver.common.by import By

# 指定 driver 路径
edge_driver_path = r"C:\Windows\System32\msedgedriver.exe"
service = Service(executable_path=edge_driver_path)

# 可选项
options = Options()
options.add_experimental_option("detach", True)  # 浏览器执行完后不自动关闭

# 启动浏览器
driver = webdriver.Edge(service=service, options=options)


driver.get("https://www.ifm.cn/cn/zh")  # 打开百度首页

title = driver.title  # 获取页面标题
print(f"页面标题: {title}")  # 打印页面标题

driver.implicitly_wait(5) # 等待页面加载

#接受全部 cookies
# accept_button = driver.find_element(By.XPATH, value='//*[@id="uc-center-container"]/div[2]/div/div[1]/div/div/button[1]')
# accept_button.click()  # 点击接受 cookies 按钮

# 搜索框定位并获取 相对路径
search_box = driver.find_element(by=By.XPATH, value='//*[@id="search-bar__input"]')

# 搜索框输入内容
search_box.send_keys("IM5135")  # 输入 "Selenium" 到搜索框

# 按enter
search_box.submit()  # 提交搜索表单，触发搜索操作


# 关闭浏览器
# driver.quit()
# IM5135   以这个型号为例
# 主页  https://www.ifm.cn/cn/zh
# 搜索框  //*[@id="search-bar__input"]