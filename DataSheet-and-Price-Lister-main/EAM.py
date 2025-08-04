# 从edge_operation import open_edge
from edge_operation import open_edge, edge_quit
# import by
from selenium.webdriver.common.by import By
import time
# import keys
from selenium.webdriver.common.keys import Keys
# import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
# import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
# import TimeoutException
from selenium.common.exceptions import TimeoutException


ERIC_HOME = 'https://eric.textron.com/'


EAM_path = 'https://eu1.eam.hxgnsmartcloud.com/web/base/logindisp?tenant=KAUTEX_PRD'


edge = open_edge(implicitly_wait=60)


# edge.get(ERIC_HOME)


# workOrder_xpath = "//*[@id='tab-1052-btnInnerEl']"
workOrderBtn_xpath = '//*[@id="tab-1052"]'
# inputNameBox_xpath = "//*[@id='textfield-1333-inputEl']"
inputNameBox_xpath = '//*[@id="textfield-1333-triggerWrap"]'



edge.get(EAM_path)

def textron_login(edge):
# 德事隆sign in
# 输入用户名
    user = 'jhu00'
    password = '@2qwertyuiop[]'  
    step = edge.find_element(by=By.XPATH, value="//input[@id='identifierInput']")
    step.send_keys(user)  

    # next按钮
    step = edge.find_element(by=By.XPATH, value="//a[@title='authentication.identifier.template. signInButtonTitle']")
    step.click()  


    # 输入密码
    time.sleep(5)  # 等待页面加载
    step = edge.find_element(by=By.XPATH, value="//input[@id='password']")
    step.send_keys(password)

    # sign on按钮
    step = edge.find_element(by=By.XPATH, value="//a[@title='html.form.login.template. signInButtonTitle']")
    step.click()

# def waitLoading_catchTag_operate(tag_xpath,edge=edge, wait_time=50, operate=1,send_key=None):
#     """等待页面加载，找到指定元素，执行操作
    
#     Args:
#         edge (webdriver.Edge): Edge浏览器对象
#         tag_xpath (str): 目标元素的xpath
#         wait_time (int, optional): 等待时间. Defaults to 30.
#         operate (int, optional): 操作类型. Defaults to 1.   1:点击  2:输入
#         send_key (str, optional): 如果是输入操作，需要输入的内容. Defaults to None."""
#     try:
#         # 目标元素
#         target_element = WebDriverWait(edge, wait_time).until(
#             EC.element_to_be_clickable((By.XPATH, tag_xpath))
#         )
#         EC.element_located_to_be_selected()
#         # 元素找到后，执行操作（如点击、获取文本）
#         match operate:
#             case 1:
#                 time.sleep(5)  # 等待页面加载
#                 target_element.click()
#             case 2:
#                 target_element.send_keys(send_key)
#             # case 3:
#             #     print("执行第三个分支")
#             # case _:
#             #     print("不匹配任何分支")
                
#     except TimeoutException:
#         print(f"超时：目标元素未在 {wait_time}秒内加载完成")
def waitLoading_catchTag_operate(tag_xpath, edge=edge, wait_time=50, operate=1, send_key=None):
    """等待页面加载，找到指定元素，执行操作"""
    try:
        # 根据操作类型选择等待条件：输入操作优先确保元素可见且存在
        if operate == 2:
            target_element = WebDriverWait(edge, wait_time).until(
                EC.visibility_of_element_located((By.XPATH, tag_xpath))  # 输入框用可见性判断更可靠
            )
        else:
            target_element = WebDriverWait(edge, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, tag_xpath))  # 点击操作保持可点击判断
            )
        
        # 执行操作
        if operate == 1:
            time.sleep(5)  # 缩短不必要的等待
            target_element.click()
        elif operate == 2 and send_key is not None:
            target_element.clear()  # 输入前清空，避免残留内容
            target_element.send_keys(send_key)
                
    except TimeoutException:
        # print web code
        print(edge.page_source)
        print(f"超时：目标元素（XPath: {tag_xpath}）未在 {wait_time}秒内加载完成")
# textron_login(edge)

# 获取work order按钮


# step = edge.find_element(by=By.XPATH, value=workOrderBtn_xpath)
# time.sleep(5)
# step.click()
print('开始获取work order按钮')
waitLoading_catchTag_operate(workOrderBtn_xpath)

# 筛选work order，根据人员
# step = edge.find_element(by=By.XPATH, value="//*[@id='textfield-1333-inputEl']")
# time.sleep(30)
# step.send_keys('HXSH')
# 回车
print('开始筛选work order')
waitLoading_catchTag_operate(inputNameBox_xpath,operate=2,send_key='HXSH')
time.sleep(5)
# step.send_keys(Keys.ENTER)

