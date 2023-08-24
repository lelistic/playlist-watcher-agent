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
    
def sleep(seconds):
    def wait(driver):
        time.sleep(seconds)
        return True
    return wait

def main(driver):
    

    driver.get(playlist_link)

    # Get video links from the playlist
    video_elements = WebDriverWait(driver, 90).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.ytd-playlist-video-renderer')))
    video_links = [element.get_attribute('href') for element in video_elements]
    for video_link in video_links:
        
        print(video_link)
        driver.get(video_link)
        jump_time = random.randint(10, 35)
        # Check if the video is playing
        play_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-play-button')
        if not play_button.get_attribute('title') == 'Pause (k)':
            # Video is paused, click the play button
            play_button.click()
        WebDriverWait(driver, 2).until(sleep(2))
        # Perform the jump using JavaScript
        driver.execute_script(f"document.querySelector('video').currentTime = {jump_time};")


        #time.sleep(180)
        # Wait for 180 seconds before proceeding
        WebDriverWait(driver, 180).until(sleep(180))
        print("-")


if __name__=='__main__':
    try:
        driver = get_driver(None)
        main(driver)
    except Exception as e1:
        print("ERROR ","|", repr(e1))
    finally:
    # Ensure the WebDriver process is terminated properly
        if driver:
            driver.quit()