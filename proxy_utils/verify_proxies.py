import time
import requests
from __init__ import is_proxy_working, get_driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Fetch a list of free proxy servers
def get_free_proxies():
    url = "https://www.sslproxies.org/"
    response = requests.get(url)
    proxies = []
    if response.status_code == 200:
        rows = response.text.split("<tr>")
        for row in rows[1:]:
            cols = row.split("</td>")
            if len(cols) >= 2:
                ip = cols[0].split(">")[1]
                port = cols[1].split(">")[1]
                proxies.append(f"{ip}:{port}")
    return proxies


def verify_1():
    final_proxy_list=[]
    internal_proxies = get_free_proxies()
    driver = None
    for proxy in internal_proxies:
        print("\nProxy: ", proxy)
        try:
            driver = is_proxy_working(proxy)
            if driver:
                print("Proxy is working!")
                final_proxy_list.append(proxy)
        except Exception as e:
            print("Proxy is not working. ==> ", repr(e))
        finally:
            if driver:
                driver.quit()
    print()
    print()
    print("Final list:")
    for p in final_proxy_list:
        print(p)    



if __name__=='__main__':
    
    
    final_proxy_list=[]
    internal_proxies = get_free_proxies()
    driver = None
    for proxy in internal_proxies:
        print("\nProxy: ", proxy)
        try:
            driver = get_driver(proxy)
            driver.get("https://www.youtube.com/watch?v=CEH-eYSlXrw")
            total_duration_element = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.CLASS_NAME, 'ytp-time-duration')))
            total_duration_text = total_duration_element.text
            total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_duration_text.split(":"))))

            
            print("Proxy is working! And video has", total_seconds, " total seconds.")
            time.sleep(60)
            final_proxy_list.append(proxy)
        except Exception as e:
            print("Proxy is not working. ==> ", repr(e))
        finally:
            if driver:
                driver.quit()
    print()
    print()
    print("Final list:")
    for p in final_proxy_list:
        print(p)  
    