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
import time

def create_driver():
    """创建并返回一个 Edge 浏览器实例"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")  # 设置日志级别
    service = Service(executable_path="DataSheet-and-Price-Lister-main/msedgedriver.exe")  # 如果 msedgedriver 在 PATH 中，无需指定路径
    driver = webdriver.Edge(service=service, options=options)
    return driver

def open_url(driver, url):
    """打开指定的网页 URL"""
    driver.get(url)

def operate_element(driver, by, value, action, input_text=None, timeout=10):
    """
    通用元素操作函数

    参数：
    - driver: selenium webdriver 实例
    - by: 定位方式（例如 By.ID, By.XPATH, By.NAME, By.CSS_SELECTOR 等）
    - value: 元素定位值
    - action: 要执行的操作，如 'click', 'send_keys', 'clear', 'get_text'
    - input_text: 输入框中要输入的内容（仅在 send_keys 操作中使用）
    - timeout: 等待时间（默认 10 秒）

    返回：
    - 如果是 get_text 或 get_attribute，则返回对应值
    - 其他操作无返回值
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))

        if action == 'click':
            element.click()
        elif action == 'send_keys':
            element.send_keys(input_text)
        elif action == 'clear':
            element.clear()
        elif action == 'get_text':
            return element.text
        elif action.startswith("get_attribute:"):
            attr = action.split(":", 1)[1]
            return element.get_attribute(attr)
        else:
            print(f"❌ Unknown action: {action}")
    except Exception as e:
        print(f"❌ Error operating element: {e}")

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
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(wait)
            else:
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




if __name__ == '__main__':

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
