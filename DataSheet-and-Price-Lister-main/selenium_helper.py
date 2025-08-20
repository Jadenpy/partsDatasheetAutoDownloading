import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver import ActionChains

class SeleniumHelper:
    def __init__(self, driver, timeout=50):
        self.driver = driver
        self.timeout = timeout

    def operate_element(self, by, value, action, input_text=None, tag_comment=None, if_scroll=False):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, value))
            )

            if if_scroll:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)

            if action == 'click':
                element.click()
            elif action == 'double_click':
                ActionChains(self.driver).double_click(element).perform()
            elif action == 'input':
                element.clear()
                element.send_keys(input_text)
            elif action == 'get_text':
                return element.text
            elif action == 'get_attribute':
                return element.get_attribute(input_text)
            elif action == 'hover':
                ActionChains(self.driver).move_to_element(element).perform()
            else:
                raise ValueError(f"Unsupported action: {action}")

            if tag_comment:
                print(f"[INFO] {tag_comment} -> {action} success")

        except TimeoutException:
            print(f"[ERROR] Timeout while waiting for element: {value}")
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"[ERROR] Interaction failed with element {value}: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error during {action} on {value}: {e}")

    def auto_retry(self, func, retries=3, wait=2):
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                print(f"[WARN] Attempt {attempt+1} failed: {e}")
                time.sleep(wait)
        raise RuntimeError(f"Function failed after {retries} retries")
