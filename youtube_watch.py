from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

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
    for _ in range(num_repeats):
        video_links = get_video_links_from_playlist(playlist_link)
        if not video_links:
            print("No videos found in the playlist.")
            break

        # Watch videos one by one
        for link in video_links[:num_videos_to_watch]:
            watch_video(link)

def watch_video(video_link):
    path_to_webdriver = '/usr/bin/chromedriver'  # Path to ChromeDriver in the Docker container
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=path_to_webdriver, options=options)

    try:
        driver.get(video_link)
        time.sleep(5)  # Wait for the video to load
        # Add additional actions if needed while watching the video

    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

# Example usage:
playlist_link = "https://www.youtube.com/playlist?list=PL1234567890"  # Replace with the desired playlist link
watch_playlist(playlist_link, num_repeats=3, num_videos_to_watch=5)
