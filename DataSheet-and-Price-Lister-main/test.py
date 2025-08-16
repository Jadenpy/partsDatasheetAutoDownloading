
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
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException,TimeoutException

import random
from datetime import datetime, timedelta

def random_weekday(start_date: str, end_date: str) -> str:
    """
    返回 start_date 和 end_date 之间的一个非周六、周日的随机日期（格式 YYYY-MM-DD）
    """
    # 转换为 datetime 对象
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    if start > end:
        raise ValueError("start_date must be earlier than or equal to end_date")
    
    # 生成所有非周六/周日的日期
    weekdays = []
    current = start
    while current <= end:
        if current.weekday() < 5:  # 0-4 表示周一到周五
            weekdays.append(current)
        current += timedelta(days=1)
    
    if not weekdays:
        raise ValueError("No weekdays available in the given range.")
    
    # 随机选择一个日期
    chosen_date = random.choice(weekdays)
    return chosen_date.strftime("%Y-%m-%d")

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

# def scroll_and_click(driver, selector):
#     elem = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, selector))
#     )
#     driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", elem)
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
#     elem.click()

def operate_element(driver, by, value, action, input_text=None, timeout=80, tag_comment=None, if_scroll= True):
    """
    通用元素操作函数

    参数：
    - driver: selenium webdriver 实例
    - by: 定位方式（例如 By.ID, By.XPATH, By.NAME, By.CSS_SELECTOR 等）
    - value: 元素定位值
    - action: 要执行的操作，如 'click', 'send_keys', 'clear', 'get_text','send_keys_and_enter','get_element','get_attribute','right_click' 等
    - input_text: 输入框中要输入的内容（仅在 send_keys 操作中使用）
    - timeout: 等待时间（默认 80 秒）
    - tag_comment: 操作注释（可选）
    - if_scroll: 是否滚动到元素位置（可选）

    返回：
    - 如果是 get_text 或 get_attribute，则返回对应值
    - 其他操作无返回值
    - 元素
    """
    try:
        wait = WebDriverWait(driver, timeout)
        
        if tag_comment:
            print(f"{datetime.now().strftime('%H:%M:%S')},等待{tag_comment}出现,{timeout}秒")
        else:
            print(f"{datetime.now().strftime('%H:%M:%S')},等待{value}出现,{timeout}秒")
        time.sleep(1.5)
        if if_scroll:
            # 元素已存在于DOM中，但可能不可见
            element = wait.until(EC.presence_of_element_located((by, value)))  
            # 滚动到元素位置
            driver.execute_script("arguments[0].scrollIntoView();", element)
            # 等待元素可见，且可交互
            element = wait.until(EC.element_to_be_clickable((by, value)))
        else:
            element = wait.until(EC.element_to_be_clickable((by, value)))
        if element:
            print(f"{datetime.now().strftime('%H:%M:%S')},元素出现")
        time.sleep(0.5)
        if action == 'click':
            element.click()
            time.sleep(0.2)
            if tag_comment:
                print(f"已经点击元素{tag_comment}")
            else:
                print(f"已经点击元素{value}")
        elif action == 'right_click':
            ActionChains(driver).context_click(element).perform()
            time.sleep(0.2)
            print(f"已右键单击元素{tag_comment or value}")
        elif action == 'send_keys':
            # element.click()
            # time.sleep(0.2)
            # element.clear()
            
            # element.send_keys(input_text)
            # time.sleep(0.2)
            element.click()
            time.sleep(0.1)
            element.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.1)
            element.send_keys(Keys.DELETE)
            time.sleep(0.1)
            element.send_keys(input_text)
            time.sleep(0.2)
            if tag_comment:
                print(f"在元素{tag_comment}已输入{input_text}")
            else:
                print(f"在元素{value}已输入{input_text}")           
        elif action == 'send_keys_and_enter':
            element.clear()
            time.sleep(0.2)
            element.send_keys(input_text)
            time.sleep(0.2)
            element.send_keys(Keys.ENTER)
            time.sleep(0.2)
            if tag_comment:
                print(f"在元素{tag_comment}已输入{input_text}并回车")
            else:
                print(f"在元素{value}已输入{input_text}并回车")
        elif action == 'clear':
            element.clear()
            time.sleep(0.2)
            if tag_comment:
                print(f"已清空元素{tag_comment} 的内容")
            else:
                print(f"已清空元素{value} 的内容")
        elif action == 'get_text':
            if tag_comment:
                print(f"已返回元素{tag_comment} 的内容")
            else:
                print(f"已返回元素{value} 的内容")
            return element.text
        elif action.startswith("get_attribute:"):
            attr = action.split(":", 1)[1]
            attr_value = element.get_attribute(attr)
            if tag_comment:
                print(f"已返回元素{tag_comment} 的内容")
                print(f"元素{tag_comment} 的属性{attr}的值为: {attr_value}")
            else:
                print(f"已返回元素{value} 的内容")
                print(f"元素{value} 的属性{attr}的值为: {attr_value}")
            return attr_value
        elif action == 'get_element':
            return element
        else:
            print(f"❌ 未知的操作: {action}")
    except Exception as e:
        # print(f"❌ 执行操作时出错: {e}")
        raise

def auto_retry(func, retries=3, wait=2,driver=None):

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
            print(f"⚠️ 尝试 {attempt} 失败: {e}, 等待 {wait} 秒后重试...{datetime.now().strftime('%H:%M:%S')}")
            if attempt < retries:
                time.sleep(wait)
                # driver.refresh()
            else:
                print(f'❌尝试 {retries} 次后仍然失败，请检查元素是否加载完成。{datetime.now().strftime("%H:%M:%S")}')
                # return None
                # 原封不动的抛出异常，让调用者处理
                raise   

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

    time.sleep(1)  # 建议用显示等待代替，这里暂时保留

    print("切换到新标签页")
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
        print(f"🔁 已找到 iframe:{iframe_value}")
        time.sleep(1)
        driver.switch_to.frame(iframe)
        print(f"🔁 已切换到 iframe: {iframe_by}")
        return driver

    except Exception as e:
        print(f"⚠️ 未找到目标iframe元素: {iframe_value}")
        driver.switch_to.default_content()
        return None


def operate_chain(driver, target_by, target_value, action, 
                  wait_time=10, input_text=None, drag_to=None, hold_seconds=1):
    """
    使用 ActionChains 执行指定动作（高鲁棒性）
    
    参数:
    - driver: Selenium WebDriver
    - target_by: 定位方式（By.ID / By.XPATH / By.CSS_SELECTOR 等）
    - target_value: 定位值
    - action: 字符串动作名
        支持:
        "click"         - 单击
        "double-click"  - 双击
        "right-click"   - 右键
        "hover"         - 悬停
        "click-hold"    - 按住（hold_seconds 秒）
        "drag"          - 拖拽到另一个元素（需传 drag_to）
        "send-keys"     - 输入文字（需传 input_text）
    - wait_time: 显式等待时间
    - input_text: 输入文字内容（send-keys 用）
    - drag_to: 拖拽目标 WebElement（drag 用）
    - hold_seconds: click-hold 按住时长（秒）
    """
    try:
        wait = WebDriverWait(driver, wait_time)
        element = wait.until(EC.presence_of_element_located((target_by, target_value)))
        element = wait.until(EC.element_to_be_clickable((target_by, target_value)))

        # 滚动到可见位置（避免 out of bounds）
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)

        actions = ActionChains(driver)

        if action == "click":
            actions.move_to_element(element).click()

        elif action == "double-click":
            actions.move_to_element(element).double_click()

        elif action == "right-click":
            actions.move_to_element(element).context_click()

        elif action == "hover":
            actions.move_to_element(element)

        elif action == "click-hold":
            actions.move_to_element(element).click_and_hold()
            time.sleep(hold_seconds)
            actions.release()

        elif action == "drag":
            if drag_to is None:
                raise ValueError("drag 动作必须提供 drag_to 参数")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", drag_to)
            actions.drag_and_drop(element, drag_to)

        elif action == "send-keys":
            if input_text is None:
                raise ValueError("send-keys 动作必须提供 input_text 参数")
            actions.move_to_element(element).click().send_keys(input_text)

        else:
            raise ValueError(f"不支持的动作: {action}")

        # 一次性执行所有动作
        actions.perform()
        # return element

    except TimeoutException:
        print(f"❌ 等待元素超时: {target_by} = {target_value}")
    except Exception as e:
        print(f"❌ 执行动作链出错: {e}")


# Selenium 4.3 模糊匹配 XPath 映射
locators = {
    # ===== WO 读取 =====
    "start_date": '//*[@id="uxdate-1412-inputEl"]',
    "end_date": '//*[@id="uxdate-1413-inputEl"]',
    "assigned_to": '//*[@id="lovfield-1414-inputEl"]',
    "status": '//*[@id="uxcombobox-1415-inputEl"]',
    "estimated_hours": '//*[@id="uxnumber-1425-inputEl"]', 

    # ===== 标签页 & 按钮类 =====
    "record_view": '//*[@id="tab-1163-btnInnerEl"]',
    "book_labor": '//*[@id="tab-1166-btnInnerEl"]',
    "record_save": '//*[@id="button-1033-btnIconEl"]',  # 支持CTRL+S
    "slide_bar": '//*[@id="panel-1093-splitter"]',
    # "submit": '//*[@id="button-1652-btnIconEl"]',
    "submit": "(//*[starts-with(@id, 'button-') and substring(@id, string-length(@id) - string-length('-btnIconEl') +1) = '-btnIconEl'])[38]", # 索引从1开始
    
    # ===== WO 输入 =====
    # "panel": '//*[@id="panel-1664-bodyWrap"]',
    # "panel": "//*[starts-with(@id, 'panel-') and substring(@id, string-length(@id) - string-length('-bodyWrap') +1) = '-bodyWrap']",
    "panel": "(//*[starts-with(@id, 'panel-') and substring(@id, string-length(@id) - string-length('-bodyWrap') +1) = '-bodyWrap'])[19]",   # 索引从1开始
    "employee": './/input[contains(@id, "lovmultiselectfield")]',
    "hours_worked": './/input[contains(@id, "uxnumber")]',
    "date_worked": './/input[contains(@id, "uxdate")]',
    "dropdown": "(//*[starts-with(@id, 'uxcombobox-') and substring(@id, string-length(@id) - string-length('-trigger-picker') +1) = '-trigger-picker'])[5]"

    
    
}




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
        try:
            # 创建 Edge 浏览器实例
            driver = create_driver()
            # 打开指定的 URL
            open_url(driver, "https://myeric.textron.com/")
            # 点击 EAM a Tag
            auto_retry(lambda: operate_element(driver, By.XPATH, '//*[@id="MyTools"]/div/ul/li[7]/a', 'click',tag_comment="EAM Tag"),driver=driver)
            # Tab 跳转
            handle_new_tab(driver)
            # 进入EAM页面后，等待页面加载,并点击 order a Tag     //*[@id="tab-1052"]
            auto_retry(lambda: operate_element(driver, By.XPATH, '//*[@id="tab-1052"]', 'click',tag_comment="WO Tag"),driver=driver)
            
            driver = get_iframe_and_return(driver,By.ID,"uxtabiframe-1040-iframeEl")
            #       !!!重点： CSS_SELECTOR 可以找到元素，且可以点击，但是XPATH不行，报警不可点击
            auto_retry(lambda: operate_element(driver,By.CSS_SELECTOR,'#textfield-1333-inputEl','send_keys_and_enter','HXSH',tag_comment="人员姓名输入框",if_scroll=True),driver=driver)
            # 找到下拉按钮并点击
            auto_retry(lambda: operate_element(driver,By.XPATH,'//*[@id="uxfilteroperator-1251"]','click',tag_comment="日期筛选条件下拉按钮"),driver=driver)
            # 找到 <= 选项并点击
            auto_retry(lambda: operate_element(driver,By.CSS_SELECTOR,'#menuitem-1256','click',tag_comment="日期筛选条件 <= 选项"),driver=driver)
            # 找到输入框
            auto_retry(lambda: operate_element(driver,By.CSS_SELECTOR,'#uxdate-1261-inputEl','send_keys_and_enter','2025-08-16',tag_comment="日期输入框"),driver=driver)
         
            time.sleep(3)
            try:
                print("获取工单列表：")
                # //*[@id="tableview-1103"]/div[3]
                # //*[@id="tableview-1103"]/div[3]//table[starts-with(@id, "tableview-1103-")]     and contains(@class, "x-grid-item") and not(contains(@class, "x-grid-item-alt"))
                wait = WebDriverWait(driver, 10)  # 最多等10秒
                wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tableview-1103"]/div[3]//table[starts-with(@id, "tableview-1103-record-")]')))
                tables = driver.find_elements(By.XPATH, '//*[@id="tableview-1103"]/div[3]//table[starts-with(@id, "tableview-1103-record-")]')
                
                 # all_orders = []  # 用于存放所有工单的内容     
                if tables:
                    
                    print(f"可见表格数量: {len(tables)}")
                    # 文件名   '工单'+time.strftime('%m%d', time.localtime())+'.html'
                    with open('工单'+time.strftime('%m%d')+'.html', 'w', encoding='utf-8') as f:
                        # 遍历列表并将每个表格的HTML写入文件
                        for index, table in enumerate(tables, start=1):
                            try:
                                # 获取表格完整HTML
                                table_html = table.get_attribute('outerHTML')
                                
                                # 写入标识和表格HTML（格式与打印时一致，便于阅读）
                                f.write(f"===== 第 {index} 个表格的HTML =====\n")
                                f.write(table_html + "\n")
                                f.write("-"*50 + "\n\n")  # 分隔线
                                
                                # 可选：同时在控制台打印进度
                                print(f"已保存第 {index} 个表格到文件")
                            except Exception as e:
                                error_msg = f"获取第 {index} 个表格的HTML时出错：{e}\n"
                                f.write(error_msg)  # 将错误信息也写入文件
                                print(error_msg)  # 将错误信息也打印到控制台
                else:
                    print("未找到工单表格")
                for index, table in enumerate(tables, start=1):
            # 获取工单列表  for index, table in enumerate(tables, start=1):
                    try:
                        # 找到这一行tr（这里只有一行）
                        tr = table.find_element(By.TAG_NAME, 'tr')
                        # 找到所有td元素（顺序对应你的注释）
                        tds = tr.find_elements(By.TAG_NAME, 'td')

                        # 按注释提取文本，去掉多余空白，替换转义字符 &nbsp; 为普通空格
                        def get_td_text(i):
                            # div 里面有文本
                            div = tds[i].find_element(By.TAG_NAME, 'div')
                            text = div.text.strip().replace('\xa0', ' ').replace('&nbsp;', ' ')
                            return text

                        print(f"工单 {index} 信息：")
                        print(f"  工单号: {get_td_text(0)}")
                        # print(f"  ？？？: {get_td_text(1)}")
                        print(f"  设备代码: {get_td_text(2)}")
                        print(f"  工单描述: {get_td_text(3)}")
                        print(f"  工单开启日期: {get_td_text(4)}")
                        print(f"  工单超期日期: {get_td_text(5)}")
                        print(f"  工单状态: {get_td_text(6)}")
                        print(f"  设备所属成本中心: {get_td_text(7)}")
                        print(f"  所属部门: {get_td_text(8)}")
                        # print(f"  所属的资产: {get_td_text(9)}")
                        # print(f"  空白字段: {get_td_text(10)}")
                        print(f"  所属人员: {get_td_text(11)}")
                        print(f"  工单类型: {get_td_text(12)}")
                        print(f"  工单重要程度: {get_td_text(13)}")
                        print(f"  所属工厂: {get_td_text(14)}")
                        print("-" * 50)
                    except Exception as e:
                        print(f"解析第 {index} 个工单时出错")
                        raise e
            except Exception as e:
                print(f"🚫 获取第 {index} 个工单时出错")
                raise e

            # 工单展开进行处理
            try:
                wait = WebDriverWait(driver, 10)
                
                for index, table in enumerate(tables, start=1):
             
                    print(f"正在处理第 {index} 个工单...")
                    # 点击当前工单（进入详情）  双击执行
                    ActionChains(driver).double_click(table).perform()
                    
                    # 1. 点击Record View Tab
                    operate_element(driver,By.XPATH, locators["record_view"],'click',tag_comment='Record View Tab')
                    
                    # 2. 获取当前tab的数据
                    # 2.1 Sched.Start Date    !!!重点：表单项目获取文本需要使用get_attribute:value  
                    start_date = operate_element(driver,By.XPATH, locators["start_date"],'get_attribute:value',tag_comment='Sched.Start Date')
                    # 2.2 Sched.End Date
                    end_date = operate_element(driver,By.XPATH, locators["end_date"],'get_attribute:value',tag_comment='Sched.End Date')
                    # 2.3 Assigned To
                    assigned_to = operate_element(driver,By.XPATH, locators["assigned_to"],'get_attribute:value',tag_comment='Assigned To')
                    # 2.4 Status
                    status = operate_element(driver,By.XPATH, locators["status"],'get_attribute:value',tag_comment='Status')
                    # 2.5 Estimated Hours
                    estimated_hours = operate_element(driver,By.XPATH, locators["estimated_hours"],'get_attribute:value',tag_comment='Estimated Hours')
                    # 3. 点击Book Labor tab
                    operate_element(driver,By.XPATH, locators["book_labor"],'click',tag_comment='Book Labor Tab')
                    time.sleep(2)

                    # operate_element(driver,By.XPATH, locators["record_view"],'click',tag_comment='Record View Tab')
                    # time.sleep(2)

                    
                    # 4. 输入工单执行信息
                    # parent element
                    parent_element = driver.find_element(By.XPATH, locators["panel"])
                    # 4.1 employee
                    parent_element.find_element(By.XPATH, locators["employee"]).send_keys(assigned_to)
                    # 4.2 Hours worked
                    parent_element.find_element(By.XPATH, locators["hours_worked"]).send_keys(estimated_hours)
                    # 4.3 Date Worked
                    worked_date = random_weekday(start_date, end_date)
                    parent_element.find_element(By.XPATH, locators["date_worked"]).send_keys(worked_date)   
                    # 5. 点击Submit
                    operate_element(driver,By.XPATH, locators["submit"],'click',tag_comment='Submit')
                    time.sleep(1)
                    # 6. 点击record save
                    operate_element(driver,By.XPATH, locators["record_save"],'click',tag_comment='Record Save')
                    # 右键点击record save ,消除弹窗
                    operate_element(driver,By.XPATH, locators["record_save"],'right_click',tag_comment='Record Save')
                    # 6-1. 点击record view
                    operate_element(driver,By.XPATH, locators["record_view"],'click',tag_comment='Record View')
                    # 6-2. 修改工单状态 open-->completed
                    operate_element(driver,By.XPATH, locators["status"],'send_keys','Completed',tag_comment='Status')
                    # 6-3. 点击save record
                    operate_element(driver,By.XPATH, locators["record_save"],'click',tag_comment='Save Record')
                    time.sleep(8)
                    # 7. 点击slide bar
                    operate_chain(driver,By.XPATH, locators["slide_bar"],'double-click')
                    time.sleep(2)
                    
               
                print(f"🟢 总计处理成功{len(tables)}个工单")
            except Exception as e:
                print(f"🚫 第 {index} 个工单输入失败: {e}")
                raise e
            
            # 回到默认内容
            # driver.switch_to.default_content()
        except Exception as e:
            print(f"🚫 EAM函数捕获异常：{e}，已终止")
            return  # ← 退出主函数（也可以改成 raise 继续向上传递）
        
    print(f'测试已经于 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} 开始')
    EAM()

    # /html/body/div[1]/div/div/div/div/div/div/div[3]/div[1]/div/div/div/div/div/div[4]/div/div[3]/table[1]

    
    
