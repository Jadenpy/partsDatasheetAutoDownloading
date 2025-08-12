from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Selenium 4.3 模糊匹配 XPath 映射
locators = {
    # ===== 工单字段输入类 =====
    "start_date": '//input[starts-with(@id, "uxdate-") and contains(@id, "inputEl")][1]',
    "end_date": '//input[starts-with(@id, "uxdate-") and contains(@id, "inputEl")][2]',
    "assigned_to": '//input[starts-with(@id, "lovfield-") and contains(@id, "inputEl")]',
    "status": '//input[starts-with(@id, "uxcombobox-") and contains(@id, "inputEl")]',
    "estimated_hours": '//input[starts-with(@id, "uxnumber-") and contains(@id, "inputEl")]', 

    # ===== 标签页 & 按钮类 =====
    "record_view": '//*[starts-with(@id, "tab-") and contains(@id, "btnInnerEl")][1]',
    "book_labor": '//*[starts-with(@id, "tab-") and contains(@id, "btnInnerEl")][2]',
    "record_save": '//*[starts-with(@id, "button-") and contains(@id, "btnIconEl")][1]',  # 支持CTRL+S
    "submit": '//*[starts-with(@id, "button-") and contains(@id, "btnIconEl")][last()]'
}




wait = WebDriverWait(driver, 10)

# 示例：填写工单开始日期
start_date_input = wait.until(EC.element_to_be_clickable((By.XPATH, locators["start_date"])))
start_date_input.clear()
start_date_input.send_keys("2025-08-12")

# 示例：点击提交按钮
submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, locators["submit"])))
submit_btn.click()
