# from selenium import webdriver
# from selenium.webdriver.edge.service import Service
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.common.by import By
# import time

# # 配置 Edge 驱动路径
# EDGE_DRIVER_PATH = "DataSheet-and-Price-Lister-main\msedgedriver.exe"  # 修改为你的实际路径

# # 创建服务与选项
# options = Options()
# # options.add_argument("--headless")  # 如果你不想显示浏览器窗口可以启用这行
# options.add_argument("--log-level=3")
# service = Service(executable_path=EDGE_DRIVER_PATH)
# driver = webdriver.Edge(service=service, options=options)

# # 打开百度
# driver.get("https://www.baidu.com")
# time.sleep(1)

# # 找到搜索框并输入关键词
# search_box = driver.find_element(By.ID, "kw")
# search_box.send_keys("Selenium 教程")

# # 找到按钮并点击
# search_button = driver.find_element(By.ID, "su")
# search_button.click()

# # 等待结果加载
# time.sleep(3)

# # 抓取前几个标题
# titles = driver.find_elements(By.CSS_SELECTOR, "h3.t")
# for i, title in enumerate(titles[:5], start=1):
#     print(f"{i}. {title.text}")

# # 关闭浏览器
# driver.quit()



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import keys
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

def create_driver():
    """创建并返回一个 Edge 浏览器实例"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")  # 设置日志级别
    options.add_experimental_option("detach", True)  # 关键，设置浏览器关闭时不退出
    service = Service(executable_path="DataSheet-and-Price-Lister-main\drives\msedgedriver.exe")  # 如果 msedgedriver 在 PATH 中，无需指定路径
    driver = webdriver.Edge(service=service, options=options)
    return driver

def open_url(driver, url):
    """打开指定的网页 URL"""
    driver.get(url)

def operate_element(driver, by, value, action, input_text=None, timeout=70):
    """
    通用元素操作函数

    参数：
    - driver: selenium webdriver 实例
    - by: 定位方式（例如 By.ID, By.XPATH, By.NAME, By.CSS_SELECTOR 等）
    - value: 元素定位值
    - action: 要执行的操作，如 'click', 'send_keys', 'clear', 'get_text'
    - input_text: 输入框中要输入的内容（仅在 send_keys 操作中使用）
    - timeout: 等待时间（默认 70 秒）

    返回：
    - 如果是 get_text 或 get_attribute，则返回对应值
    - 其他操作无返回值
    """
    try:
        wait = WebDriverWait(driver, timeout)
        print(f"现在是{datetime.now().strftime('%H:%M:%S')},等待元素 {by}={value} 出现,timeout={timeout}秒")
        # element = wait.until(EC.presence_of_element_located((by, value)))
        element = wait.until(EC.element_to_be_clickable((by, value)))
        print(f"现在是{datetime.now().strftime('%H:%M:%S')},元素 {by}={value} 出现")
        # time.sleep(5)
        if action == 'click':
            element.click()
            print(f"点击元素 {by}={value}")
        elif action == 'send_keys':
            element.send_keys(input_text)
            print(f"在元素 {by}={value} 输入 {input_text}")
        elif action == 'clear':
            element.clear()
            print(f"清空元素 {by}={value} 的内容")
        elif action == 'get_text':
            return element.text
        elif action.startswith("get_attribute:"):
            attr = action.split(":", 1)[1]
            return element.get_attribute(attr)
        else:
            print(f"❌ Unknown action: {action}")
    except Exception as e:
        print(f"❌ Error operating element: {e}")
        raise

def auto_retry(func, retries=3, wait=2):

    """
    Retry any function if it raises an exception.

    Parameters:
    - func: the function you want to retry (wrapped in lambda or no-arg form)
    - retries: how many times to retry
    - wait: seconds to wait between retries

    Returns:
    - the result of the function if successful
    - None if all retries fail
    """
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e},now is {datetime.now().strftime('%H:%M:%S')}")
            if attempt < retries:
                time.sleep(wait)
            else:
                print(f'now is {datetime.now().strftime("%H:%M:%S")}')
                print("❌ All retries failed.")

                return None

def expand_shadow_element(driver, element):
    """
    用于获取一个元素的 Shadow Root 对象。
    
    参数:
        driver: WebDriver 实例
        element: shadow host 元素（即包含 shadow DOM 的标签）
    
    返回:
        Shadow root 对象，可以继续用来查找内部元素
    """
    return driver.execute_script("return arguments[0].shadowRoot", element)

    # # 示例使用：
    # # 假设我们已经创建好 driver，并打开网页

    # # 1. 找到 shadow host（外部包裹 Shadow DOM 的元素）
    # shadow_host = driver.find_element(By.CSS_SELECTOR, "custom-element")

    # # 2. 获取 shadow root
    # shadow_root = expand_shadow_element(driver, shadow_host)

    # # 3. 在 shadow root 内部查找目标元素（比如按钮）
    # target_button = shadow_root.find_element(By.CSS_SELECTOR, "button.submit")

    # # 4. 操作目标元素
    # target_button.click()

def click_shadow_element(driver, shadow_host_selector, target_selector):
    """
    封装点击 Shadow DOM 内部元素的函数

    参数:
        driver: WebDriver 实例
        shadow_host_selector: shadow host 的 CSS 选择器
        target_selector: 目标元素在 Shadow DOM 中的 CSS 选择器

    功能:
        自动展开 shadow DOM 并点击内部指定元素
    """
    shadow_host = driver.find_element(By.CSS_SELECTOR, shadow_host_selector)
    shadow_root = expand_shadow_element(driver, shadow_host)
    target_element = shadow_root.find_element(By.CSS_SELECTOR, target_selector)
    target_element.click()


def handle_new_tab(driver, expected_tabs=2, timeout=50):
    """
    处理新标签页并切换到该标签页

    参数:
        driver: WebDriver 实例
        expected_tabs: 期望窗口数量，默认2个
        timeout: 等待超时时间，默认10秒

    功能:
        等待新标签页打开，并切换到该标签页
    """
    # 等待新标签页打开
    WebDriverWait(driver, timeout).until(EC.number_of_windows_to_be(expected_tabs))

    # 获取所有窗口句柄
    window_handles = driver.window_handles

    # 切换到新标签页（默认切换到最后一个）
    driver.switch_to.window(window_handles[-1])

    time.sleep(2)  # 建议用显示等待代替，这里暂时保留

    # 这里可以继续写在新标签页要做的操作


def switch_to_iframe_with_element(driver, iframe_xpath, target_by, target_value, timeout=50):
    """
    尝试切换到包含目标元素的 iframe

    参数:
        driver: WebDriver 实例
        iframe_xpath: iframe 的 XPath
        target_by: 目标元素的定位方式（如 By.XPATH, By.ID 等）
        target_value: 目标元素的定位值
        timeout: 等待目标元素出现的最长时间（秒）

    返回:
        True：成功切换到包含目标元素的 iframe
        False：所有 iframe 中都未找到目标元素
    """
    
    try:
        iframe = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, iframe_xpath))
        )
        print(f"🔁 已找到 iframe: {iframe_xpath}")
        time.sleep(2)
        driver.switch_to.frame(iframe)
        print(f"🔁 已切换到 iframe: {iframe_xpath}")

        # 在当前 iframe 查找目标元素
        print(f"🔍 正在查找目标元素: 定位方式: {target_by}, 定位值: {target_value}")
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((target_by, target_value))
        )
        print(f"✅ 找到目标元素: {target_by}, {target_value}")
        return True
    except Exception as e:
        print(f"⚠️ 在 iframe {iframe_xpath} 中未找到目标元素: {e}")
        driver.switch_to.default_content()
        return False
   
def get_iframe_and_return(driver, iframe_by, iframe_value, timeout=50):
    """
    尝试切换到包含目标元素的 iframe

    参数:
        driver: WebDriver 实例
        iframe_by: iframe 的 定位方式（如 By.XPATH, By.ID 等）
        iframe_value: iframe 的定位值
        timeout: 等待目标元素出现的最长时间（秒）

    返回:
        driver：成功切换到目标iframe
        none：未找到iframe
    """
    
    try:
        iframe = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((iframe_by, iframe_value)))
        print(f"🔁 已找到 iframe: {iframe_by}, {iframe_value}")
        time.sleep(2)
        driver.switch_to.frame(iframe)
        print(f"🔁 已切换到 iframe: {iframe_by}")
        return driver

        # 在当前 iframe 查找目标元素
        print(f"🔍 正在查找目标元素: 定位方式: {target_by}, 定位值: {target_value}")
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((target_by, target_value))
        )
        print(f"✅ 找到目标元素: {target_by}, {target_value}")
        return True
    except Exception as e:
        print(f"⚠️ 未找到目标元素: {iframe_by}, {iframe_value}")
        driver.switch_to.default_content()
        return None

def init_driver():
    options = Options()
    options.add_argument('--start-maximized')
    service = Service('msedgedriver.exe')  # 替换为你的驱动路径
    driver = webdriver.Edge(service=service, options=options)
    return driver

def wait_for_element(driver, by, value, timeout=20):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def switch_to_iframe(driver, iframe_index=0):
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > iframe_index:
        driver.switch_to.frame(iframes[iframe_index])
    else:
        raise Exception("❌ 指定 iframe 索引不存在")



if __name__ == '__main__':

    def baidu_search():
        # 创建 Edge 浏览器实例
        driver = create_driver()

        # 打开指定的 URL
        open_url(driver, "https://www.baidu.com")

        # 等待页面加载
        time.sleep(2)

        # 操作搜索框，输入关键词并提交
        auto_retry(lambda: operate_element(driver, By.ID, "kw", 'send_keys', input_text="AI真是太棒了！"))
        operate_element(driver, By.ID, "su", 'click')

        # 等待搜索结果加载
        time.sleep(3)

        # 获取并打印前几个搜索结果标题
        titles = driver.find_elements(By.CSS_SELECTOR, "h3.t")
        for i, title in enumerate(titles[:5], start=1):
            print(f"{i}. {title.text}")

        # 关闭浏览器
        driver.quit()


    # baidu_search()

    def EAM():
         # 创建 Edge 浏览器实例
        driver = create_driver()

        # 打开指定的 URL
        open_url(driver, "https://myeric.textron.com/")

        # 等待页面加载
        time.sleep(2)

        # 点击 EAM a Tag
        auto_retry(lambda: operate_element(driver, By.XPATH, '//*[@id="MyTools"]/div/ul/li[7]/a', 'click'))

        # Tab 跳转
        handle_new_tab(driver)

        # 进入EAM页面后，等待页面加载,并点击 order a Tag     //*[@id="tab-1052"]
        auto_retry(lambda: operate_element(driver, By.XPATH, '//*[@id="tab-1052"]', 'click'))
       

        print('开始处理iframe')
        iframe = WebDriverWait(driver, 70).until(
        EC.presence_of_element_located((By.ID, "uxtabiframe-1040-iframeEl"))
)
        
        driver.switch_to.frame(iframe)

        input_box_name = WebDriverWait(driver, 70).until(
        EC.presence_of_element_located((By.ID, "textfield-1333-inputEl"))
)

        print('开始输入HXSH')
       
        actions = ActionChains(driver)
        print('输入并点击')
        actions.move_to_element(input_box_name).click()
        print('回车')
        actions.send_keys("HXSH").send_keys(Keys.ENTER)
        actions.perform()
        
        
        # 找到下拉按钮并点击
        drop_down_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,'#uxfilteroperator-1251'))
)
        drop_down_btn.click()

        # 选项菜单可能是动态出现，等待选项可点击后点击
        less_than_or_equals = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#menuitem-1256'))
        )
        less_than_or_equals.click()

        # 找到输入框
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#uxdate-1261-inputEl'))
        )

        # 清空并输入日期
        input_box.clear()
        input_box.send_keys('2025-08-06')

        # 触发输入事件和回车，Selenium 不直接触发 JS 事件，但 send_keys 会触发大多数事件
        input_box.send_keys(Keys.ENTER)
    # input_box.send_keys(Keys.RETURN)
    #日期类型 2025-08-06
        # schedule end date 筛选
        # value
        """
        print('开始定位日期输入框')
        input_box_endDate = WebDriverWait(driver, 70).until(
        EC.presence_of_element_located((By.ID, "uxdate-1261-inputEl"))
        )
        print('找到输入日期框')

        # 回到默认内容
        # driver.switch_to.default_content()
        """
    print(f'测试已经于 {datetime.now()} 开始')
    EAM()

    
    
