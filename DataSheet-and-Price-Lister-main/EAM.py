# 从edge_operation import open_edge
from edge_operation import open_edge, edge_quit
# import by
from selenium.webdriver.common.by import By
import time

ERIC_HOME = 'https://eric.textron.com/'

# EAM_path =  'https://eu1.eam.hxgnsmartcloud.com/web/base/logindisp?tenant=KAUTEX_PRD'
# EAM_path =  'https://eu1.eam.hxgnsmartcloud.com/web/base/COMMON'
EAM_path = 'https://eu1.eam.hxgnsmartcloud.com/sso/samlconnect?service=https%3A%2F%2Feu1.eam.hxgnsmartcloud.com%3A443%2Fweb%2Fbase%2Fssoservlet%3Ftenant%3DKAUTEX_PRD'


edge = open_edge()


# edge.get(ERIC_HOME)


workOrder_xpath = "//*[@id='tab-1052-btnInnerEl']"




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



# textron_login(edge)