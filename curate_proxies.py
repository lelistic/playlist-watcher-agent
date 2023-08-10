import requests

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


def get_curated_proxies(proxy_urls):

    curated_proxies = []

    for proxy in proxy_urls:
        proxies = {"http": proxy, "https": proxy}
        try:
            response = requests.get('https://www.google.com', proxies=proxies, timeout=9)
            if response.status_code == 200:
                curated_proxies.append(proxy)
                print(f"Proxy {proxy} is functional and active. Added to curated list.")
            else:
                print(f"Proxy {proxy} responded with status code {response.status_code}. Discarding proxy.")
        except Exception as e:
            print(f"Proxy {proxy} is not functional or active. Discarding proxy: {e}")

    return curated_proxies

initial_proxies = get_free_proxies()
curated_proxies = get_curated_proxies(initial_proxies)

# Export the curated list of proxies to a file
with open('curated_proxies.txt', 'w') as f:
    for proxy in curated_proxies:
        f.write(proxy + '\n')
