from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Optional, Type
# import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def get_browser_driver(
    browser_type: str = "chrome",
    driver_path: Optional[str] = None,
    options: Optional[Type[webdriver.ChromeOptions | webdriver.EdgeOptions | webdriver.FirefoxOptions]] = None
) -> webdriver.Chrome | webdriver.Edge | webdriver.Firefox:
    """
    封装浏览器驱动，支持Chrome、Edge、Firefox
    
    Args:
        browser_type: 浏览器类型，支持"chrome"、"edge"、"firefox"
        driver_path: 驱动路径，为None时使用环境变量中的驱动
        options: 浏览器配置选项，为None时使用默认配置
    
    Returns:
        初始化后的浏览器驱动对象
    """
    # 初始化默认配置
    if options is None:
        if browser_type.lower() == "chrome":
            options = ChromeOptions()
            # 默认配置示例：禁用自动化控制提示、无头模式（按需开启）
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_argument("--disable-blink-features=AutomationControlled")
            # options.add_argument("--headless=new")  # 无头模式（无界面运行）
            
        elif browser_type.lower() == "edge":
            options = EdgeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
        elif browser_type.lower() == "firefox":
            options = FirefoxOptions()
            # Firefox默认配置示例
            options.set_preference("dom.webdriver.enabled", False)
            
        else:
            raise ValueError(f"不支持的浏览器类型：{browser_type}，支持'chrome'、'edge'、'firefox'")
    
    # 初始化驱动
    
    if browser_type.lower() == "chrome":
        driver = webdriver.Chrome(executable_path=driver_path, options=options) if driver_path else webdriver.Chrome(options=options)
    
    elif browser_type.lower() == "edge":
        service = EdgeService(executable_path=driver_path) if driver_path else None
        driver = webdriver.Edge(service=service, options=options) if service else webdriver.Edge(options=options)
        
    
    elif browser_type.lower() == "firefox":
        driver = webdriver.Firefox(executable_path=driver_path, options=options) if driver_path else webdriver.Firefox(options=options)
    
    return driver


# 使用示例
if __name__ == "__main__":
    # 1. 使用默认配置的Chrome浏览器
    # driver = get_browser_driver(browser_type="chrome")
    # driver.get("https://www.baidu.com")
    # print("Chrome标题：", driver.title)
    # driver.quit()
    
    # 2. 自定义Edge配置（如设置窗口大小）
    edge_options = EdgeOptions()
    edge_options.add_argument("--window-size=1200,800")
    driver = get_browser_driver(browser_type="edge",driver_path='C:\Users\jhu00\OneDrive-Textron\Documents\code\DataSheet-and-Price-Lister-main\DataSheet-and-Price-Lister-main\AI\msedgedriver.exe')
    driver.get("https://www.bing.com")
    print("Edge标题：", driver.title)
    driver.quit()
    
    # 3. 指定Firefox驱动路径（适用于驱动未在环境变量中的情况）
    # driver = get_browser_driver(browser_type="firefox", driver_path="D:/geckodriver.exe")
    # driver.get("https://www.mozilla.org")
    # driver.quit()