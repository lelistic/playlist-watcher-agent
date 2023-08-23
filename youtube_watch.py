# youtube watcher - simple version
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

from proxy_utils import get_driver ,curated_proxies
import time

import random
playlist_link = "https://www.youtube.com/playlist?list=PLMrlsG9QD-qixBzZurP7cv54lCzoSFmEo"
#playlist_link = "https://www.youtube.com/playlist?list=PLMrlsG9QD-qgy7cWdalPDz7MgCqkLTUPs"
    
def main():
    driver = get_driver(None)

    driver.get(playlist_link)

    # Get video links from the playlist
    video_elements = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.ytd-playlist-video-renderer')))
    video_links = [element.get_attribute('href') for element in video_elements]
    for video_link in video_links:
        try:
            driver.get(video_link)
            time.sleep(180)
        
        except Exception as e1:
            print("ERROR ","|", repr(e1))



if __name__=='__main__':
    main()
    