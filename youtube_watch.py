from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys

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

def watch_playlist(playlist_link, num_repeats=1, num_videos_to_watch=5):
    video_links = get_video_links_from_playlist(playlist_link)
    total_videos = len(video_links)

    for repeat in range(num_repeats):
        print(f"\n---- Repeat #{repeat + 1} ----")

        for video_number, video_link in enumerate(video_links, start=1):
            print(f"\nVideo {video_number}/{total_videos}: {video_link}")
            watch_video(video_link, video_number)  # Pass video_number as argument
            time.sleep(5)  # Wait for 5 seconds between videos




def watch_video(video_link, video_number):
    path_to_webdriver = '/usr/bin/chromedriver'  # Path to ChromeDriver in the Docker container
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(executable_path=path_to_webdriver, options=options)
    driver.set_page_load_timeout(10)  # Set page load timeout to 10 seconds (adjust as needed)

    try:
        driver.get(video_link)
        
        # Extract the video duration from the page
        video_duration = driver.find_element(By.CSS_SELECTOR, '.ytp-time-duration').text
        total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(video_duration.split(":"))))
        
        print(f"Watching Video {video_number}: {video_link}")
        print(f"Video Duration: {video_duration} (Total seconds: {total_seconds})")
        
        # Wait for the total duration of the video
        for seconds_left in range(total_seconds, 0, -1):
            sys.stdout.write(f"\rTime left: {seconds_left} seconds")
            sys.stdout.flush()
            time.sleep(1)
        
        print("\nVideo watched successfully!")

    except Exception as e:
        print(f"An error occurred while watching Video {video_number}: {e}")
    finally:
        driver.quit()


# Example usage:
playlist_link = "https://www.youtube.com/playlist?list=PLMrlsG9QD-qixBzZurP7cv54lCzoSFmEo"#"https://www.youtube.com/playlist?list=PL1234567890"  # Replace with the desired playlist link
watch_playlist(playlist_link, num_repeats=15, num_videos_to_watch=5)
