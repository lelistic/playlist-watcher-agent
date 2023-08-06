from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys
from datetime import datetime
import random
import requests

# Initialize a dictionary to store the number of views for each video
video_views = {}

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



def get_video_links_from_playlist(playlist_link):
    path_to_webdriver = '/usr/bin/chromedriver'  # Path to ChromeDriver in the Docker container
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=path_to_webdriver, options=options)

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
        video_links = []
    finally:
        driver.quit()

    return video_links

# Function to calculate the final cooldown duration based on various factors
def calculate_cooldown_duration(video_link, proxy=None):
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


def watch_video(video_link, video_number):
    path_to_webdriver = '/usr/bin/chromedriver'  # Path to ChromeDriver in the Docker container
    options = webdriver.ChromeOptions()

    options.add_argument('--headless')  # Run Chrome headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(executable_path=path_to_webdriver, options=options)
    driver.set_page_load_timeout(10)  # Set page load timeout to 10 seconds (adjust as needed)

    proxies = get_free_proxies()

    retries = 0
    max_retries = 3
    while retries < max_retries:
        try:
            proxy = random.choice(proxies)
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')

            driver.get(video_link)
            
            # Extract the video duration from the page
            duration_element = driver.find_element(By.CSS_SELECTOR, '.ytp-time-duration')
            video_duration = duration_element.text
            total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(video_duration.split(":"))))
            
            print(f"Watching Video {video_number}: {video_link} with Proxy {proxy}")
            print(f"Video Duration: {video_duration} (Total seconds: {total_seconds})")
            
            # Wait for the total duration of the video
            for seconds_left in range(total_seconds, 0, -1):
                sys.stdout.write(f"\rTime left: {seconds_left} seconds")
                sys.stdout.flush()
                time.sleep(1)
            
            print("\nVideo watched successfully!")
            return True  # Proxy worked successfully

        except Exception as e:
            print(f"An error occurred while watching Video {video_number} with Proxy {proxy}: {e}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying video {video_number} with a new proxy...\n")
            else:
                print(f"Reached maximum retries for video {video_number}. Moving on to the next video.\n")
                return False  # Proxy didn't work after max retries
        finally:
            driver.quit()

    return False  # Proxy didn't work even after retries


if __name__=='__main__':
    playlist_link = "https://www.youtube.com/playlist?list=PLMrlsG9QD-qixBzZurP7cv54lCzoSFmEo"#"https://www.youtube.com/playlist?list=PL1234567890"  # Replace with the desired playlist link
    video_links = get_video_links_from_playlist(playlist_link)
    total_videos = len(video_links)


    # Shuffle the order of videos in the playlist for better diversification
    random.shuffle(video_links)

    for video_number, video_link in enumerate(video_links):
        proxy = None

        cooldown_duration = calculate_cooldown_duration(video_link, proxy)

        print(f"\nVideo {video_number+1}/{total_videos}: {video_link}")
        print(f"Cooldown: {cooldown_duration} seconds")
        if not watch_video(video_link, video_number + 1):
            print(f"All proxies failed for video {video_number + 1}. Skipping to the next video.")
        else:
            # Update the views count for the video
            video_views[video_link] = video_views.get(video_link, 0) + 1

            time.sleep(cooldown_duration)