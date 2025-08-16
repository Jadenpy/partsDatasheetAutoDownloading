from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SeleniumHelper:
    def __init__(self, driver, timeout=20, retries=3, wait=2):
        """
        :param driver: selenium webdriver 实例
        :param timeout: 显式等待时间
        :param retries: 自动重试次数
        :param wait: 重试间隔秒数
        """
        self.driver = driver
        self.timeout = timeout
        self.retries = retries
        self.wait = wait

    def auto_retry(self, func, *args, **kwargs):
        """自动重试装饰器"""
        last_exception = None
        for attempt in range(self.retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                print(f"[Retry {attempt+1}/{self.retries}] 出错: {e}")
                time.sleep(self.wait)
        raise last_exception

    def operate_element(self, by, value, action="click", input_text=None):
        """
        通用元素操作
        :param by: 定位方式 (By.ID, By.XPATH, By.CSS_SELECTOR)
        :param value: 定位表达式
        :param action: 操作类型 ['click', 'input', 'double_click', 'gettext']
        :param input_text: 输入的文本 (仅 input 时使用)
        """
        def _action():
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, value))
            )

            if action == "click":
                element.click()
                return True
            elif action == "input":
                element.clear()
                element.send_keys(input_text)
                return True
            elif action == "double_click":
                ActionChains(self.driver).double_click(element).perform()
                return True
            elif action == "gettext":
                return element.text
            else:
                raise ValueError(f"不支持的操作: {action}")

        return self.auto_retry(_action)

    def operate_tag(self, parent_element, locator, action="click", input_text=None):
        """
        在父元素下操作子元素 (比如 ExtJS 复杂 DOM 结构)
        :param parent_element: 已找到的父元素
        :param locator: 子元素 XPath 或 CSS
        :param action: ['click', 'input', 'double_click', 'gettext']
        :param input_text: 输入内容 (input时用)
        """
        def _action():
            element = parent_element.find_element(By.XPATH, locator)

            if action == "click":
                element.click()
                return True
            elif action == "input":
                element.clear()
                element.send_keys(input_text)
                return True
            elif action == "double_click":
                ActionChains(self.driver).double_click(element).perform()
                return True
            elif action == "gettext":
                return element.text
            else:
                raise ValueError(f"不支持的操作: {action}")

        return self.auto_retry(_action)
