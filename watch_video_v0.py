
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import ElementClickInterceptedException

from proxy_utils import get_driver ,curated_proxies
import time

import random

def watch_video(video_link, video_number):
    
    internal_proxies = curated_proxies.copy()
    driver = None
    proxy = random.choice(internal_proxies)
    
    result_ = False
       
    driver = get_driver(proxy)
    try:
        driver.get(video_link)
        
        # Extract the video duration from the page
        total_duration_element = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.CLASS_NAME, 'ytp-time-duration')))
        total_duration_text = total_duration_element.text
        total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_duration_text.split(":"))))


        print(f"Watching Video {video_number}: {video_link} with Proxy {proxy}")
        print(f"Video Total seconds: {total_seconds}")

        # Check if the video is playing or paused
        is_playing = driver.execute_script(
            "return document.querySelector('.html5-video-player').paused === false;"
        )

        if not is_playing:
            try:
                # Click the video play button to start playback
                play_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.ytp-large-play-button')))
                #play_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-large-play-button')
                play_button.click()
            except ElementClickInterceptedException as e1:
                if 'yt-upsell-dialog-renderer' in repr(e1):
                    print("Detected an upsell dialog, attempting to close...")
                    driver.execute_script('document.querySelector(".yt-upsell-dialog-renderer").style.display = "none";')
                    print("Upsell dialog closed. Trying click again...")
                    play_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.ytp-large-play-button')))
                    play_button.click()
                else:
                    raise e1

        # Calculate a random start point within the range of 22% to 47%
        start_point = total_seconds * 0.22 + (total_seconds * 0.25 * random.random())
        
        # Seek to the calculated start point
        progress_bar = play_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ytp-progress-bar')))
        #progress_bar = driver.find_element(By.CLASS_NAME, 'ytp-progress-bar')
        progress_element = progress_bar.find_element(By.CLASS_NAME, 'ytp-play-progress')
        progress_width = start_point / total_seconds
        driver.execute_script("arguments[0].style.transform = 'scaleX({})'".format(progress_width), progress_element)

        # Check if the video is playing or paused
        is_playing = driver.execute_script(
            "return document.querySelector('.html5-video-player').paused === false;"
        )

        if not is_playing:
            try:
                # Click the video play button to start playback
                play_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.ytp-large-play-button')))
                #play_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-large-play-button')
                play_button.click()
            except ElementClickInterceptedException as e2:
                if 'yt-upsell-dialog-renderer' in repr(e2):
                    print("Detected an upsell dialog, attempting to close...")
                    driver.execute_script('document.querySelector(".yt-upsell-dialog-renderer").style.display = "none";')
                    print("Upsell dialog closed. Trying click again...")
                    play_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.ytp-large-play-button')))
                    play_button.click()
                else:
                    raise e2

        print("Watching video with Proxy:", proxy)
        print("Video started from {:.2f}%".format(start_point / total_seconds * 100))
        
        # Wait for the total duration of the video
        time.sleep(total_seconds - int(start_point)+1)
        
        print("\nVideo watched successfully!")
        result_ = True  # Proxy worked successfully
        

    except Exception as e3:
        print("Error trying to watch video", video_number, "with Proxy",proxy,"|", repr(e3))
    finally:
        if driver:
            driver.quit()
    return result_

