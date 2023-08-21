import requests
from __init__ import is_proxy_working
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

if __name__=='__main__':
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
        