from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
path_to_webdriver = '/usr/bin/chromedriver'  # Path to ChromeDriver in the Docker container
def get_curated_proxies_from_file():
    curated_proxies = []

    with open('curated_proxies.txt', 'r') as f:
        for line in f:
            curated_proxies.append(line.strip())

    return curated_proxies

curated_proxies = get_curated_proxies_from_file()

def get_driver(proxy):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    if proxy:
        options.add_argument('--proxy-server={}'.format(proxy))  # Apply proxy for both HTTP and HTTPS

    # Initiate ChromeDriver with the same options and proxy configuration
    driver = webdriver.Chrome(executable_path=path_to_webdriver, options=options)
    driver.set_page_load_timeout(10)  # Set page load timeout to 10 seconds (adjust as needed)
    return driver

def is_proxy_working(proxy):
    driver = get_driver(proxy)
    driver.get("https://ifconfig.me/ip")
    result_ = None
    try:
        html = driver.page_source
        time.sleep(2)
        print(html)
        ip_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/pre")))
        ip_address = ip_element.get_attribute('textContent').strip()

        print(ip_address,proxy.split(':')[0])
        result_ = driver
    except Exception as e1:
        print("An error occurred while checking proxy:", repr(e1))    
    return result_ 


