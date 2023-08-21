
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from proxy_utils import get_driver, curated_proxies
import time

from datetime import datetime
import random

# Initialize a dictionary to store the number of views for each video
video_views = {}

def get_video_links_from_playlist(playlist_link):
    driver = get_driver(None)
    video_links = []
    try:
        driver.get(playlist_link)
        time.sleep(5)  # Wait for the page to load

        # Scroll down to load more videos (repeat this if needed)
        for _ in range(3):
            driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
            time.sleep(2)

        # Get video links from the playlist
        video_elements = driver.find_elements(By.CSS_SELECTOR, 'a.ytd-playlist-video-renderer')
        video_links = [element.get_attribute('href') for element in video_elements]

    except Exception as e:
        print("An error occurred:", e)
        
    finally:
        driver.quit()

    return video_links

def calculate_cooldown_duration(video_link):
    """Function to calculate the final cooldown duration based on various factors"""
    
    # Apply dynamic adjustment to cooldown calculation based on real-time feedback
    min_cooldown = 10
    max_cooldown = 30
    cooldown_duration = max_cooldown - (video_views.get(video_link, 0) * 2)
    cooldown_duration = max(min(cooldown_duration, max_cooldown), min_cooldown)

    # Introduce randomness to cooldown duration
    cooldown_duration += random.randint(10, 20)

    # Introduce time-based variation (Overall pacing mechanism)
    now = datetime.now()
    hour = now.hour

    if hour >= 17:  # After 5 pm
        cooldown_duration += random.randint(5, 10)
    else:  # In the morning
        cooldown_duration += random.randint(15, 30)

    return cooldown_duration

def get_video_duration(driver):
    try:
        duration_text = driver.find_element(By.CSS_SELECTOR, '.ytp-time-duration').text
        minutes, seconds = map(int, duration_text.split(':'))
        return minutes * 60 + seconds
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return 1

def watch_video(video_link, video_number):
    
    internal_proxies = curated_proxies.copy()
    driver = None
    proxy = random.choice(internal_proxies)
    print("Proxy: ", proxy)
    result_ = False
    try:
        
        
        driver = get_driver(proxy)
        
        retries = 0
        max_retries = 3
        while retries < max_retries:
        
            try:
                driver.get(video_link)
                
                # Extract the video duration from the page
                total_seconds = get_video_duration(driver)
                
                print(f"Watching Video {video_number}: {video_link} with Proxy {proxy}")
                print(f"Video Total seconds: {total_seconds}")
                
                # Check if the video is playing or paused
                is_playing = driver.execute_script(
                    "return document.querySelector('.html5-video-player').paused === false;"
                )

                if not is_playing:
                    # Click the video play button to start playback
                    play_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-large-play-button')
                    play_button.click()

                # Find the total duration of the video
                total_duration_element = driver.find_element(By.CLASS_NAME, 'ytp-time-duration')
                total_duration_text = total_duration_element.text
                total_duration_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_duration_text.split(":"))))

                # Calculate a random start point within the range of 22% to 47%
                start_point = total_duration_seconds * 0.22 + (total_duration_seconds * 0.25 * random.random())
                
                # Seek to the calculated start point
                progress_bar = driver.find_element(By.CLASS_NAME, 'ytp-progress-bar')
                progress_element = progress_bar.find_element(By.CLASS_NAME, 'ytp-play-progress')
                progress_width = start_point / total_duration_seconds
                driver.execute_script("arguments[0].style.transform = 'scaleX({})'".format(progress_width), progress_element)

                print("Watching video with Proxy:", proxy)
                print("Video started from {:.2f}%".format(start_point / total_duration_seconds * 100))
                
                # Wait for the total duration of the video
                time.sleep(total_duration_seconds)
                
                print("\nVideo watched successfully!")
                result_ = True  # Proxy worked successfully
                break

            except Exception as e:
                print(f"An error occurred while watching Video {video_number} with Proxy {proxy}: {e}")
                internal_proxies.remove(proxy)
                retries += 1
                if retries < max_retries:
                    print(f"Retrying video {video_number} with a new proxy...\n")
                    if driver:
                        driver.quit()  # Quit the current driver
                    proxy = random.choice(internal_proxies)
                    driver = get_driver(proxy)
                else:
                    print(f"Reached maximum retries for video {video_number}. Moving on to the next video.\n")
                    if driver:
                        driver.quit()
                    # Proxy didn't work after max retries
    finally:
        if driver:
            driver.quit()

    return result_  # Proxy didn't work even after retries


if __name__=='__main__':
    playlist_link = "https://www.youtube.com/playlist?list=PLMrlsG9QD-qixBzZurP7cv54lCzoSFmEo"
    #playlist_link = "https://www.youtube.com/playlist?list=PLMrlsG9QD-qgy7cWdalPDz7MgCqkLTUPs"
    video_links = get_video_links_from_playlist(playlist_link)
    total_videos = len(video_links)


    # Shuffle the order of videos in the playlist for better diversification
    random.shuffle(video_links)

    for video_number, video_link in enumerate(video_links):
        

        cooldown_duration = calculate_cooldown_duration(video_link)

        print(f"\nVideo {video_number+1}/{total_videos}: {video_link}")
        print(f"Cooldown: {cooldown_duration} seconds")
        if not watch_video(video_link, video_number + 1):
            print(f"All proxies failed for video {video_number + 1}. Skipping to the next video.")
        else:
            # Update the views count for the video
            video_views[video_link] = video_views.get(video_link, 0) + 1

            time.sleep(cooldown_duration)