
## YouTube Playlist Watcher - Expert Agent made by chatGPT 3.5

**WARNING:** Please, be responsible and only use this code for educational purposes 

This documentation summarizes the steps required to create the Python script and Dockerfile for automating YouTube playlist watching. Use this information to understand the implementation and to properly set up the environment to run the script.

This is a Python script that automates the process of watching videos from a YouTube playlist using the `selenium` library. The script fetches video links from the playlist and repeatedly watches the specified number of videos from the playlist.

### Prerequisites

- Python 3.8 or later
- Docker (if you want to run the script in a Docker container)

### Python Script

Create a Python script named `youtube_watch.py` with the following content:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_video_links_from_playlist(playlist_link):
    # ... (refer to the provided code in the previous answer)

def watch_playlist(playlist_link, num_repeats=1, num_videos_to_watch=5):
    # ... (refer to the provided code in the previous answer)

def watch_video(video_link):
    # ... (refer to the provided code in the previous answer)
```

### Docker Configuration

Create a file named `Dockerfile` with the following content:

```Dockerfile
# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y wget unzip curl

# Download and install Chrome browser
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Download and install ChromeDriver
ARG CHROME_DRIVER_VERSION=94.0.4606.61
RUN wget -q -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/ && \
    rm /tmp/chromedriver.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY youtube_watch.py .

# Set environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Run the Python script
CMD ["python", "youtube_watch.py"]
```

### Requirements

Create a file named `requirements.txt` with the following content:

```
selenium==3.141.0
```

### Usage

To run the script locally without Docker:

1. Make sure you have Python 3.8 or later installed.
2. Install the required Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

3. Update the `playlist_link`, `num_repeats`, and `num_videos_to_watch` variables in `youtube_watch.py` with the appropriate values.
4. Execute the script:

   ```bash
   python youtube_watch.py
   ```

To run the script within a Docker container:

1. Build the Docker image using the provided Dockerfile:

   ```bash
   docker build -t youtube_agent .
   ```

2. Update the `playlist_link`, `num_repeats`, and `num_videos_to_watch` variables in `youtube_watch.py` with the appropriate values.
3. Run the Docker container:

   ```bash
   docker run --name youtube_agent_container youtube_agent
   ```

**Note:** Make sure to replace `https://www.youtube.com/playlist?list=PL1234567890` in the `playlist_link` variable with the link to your desired playlist. The `num_repeats` variable determines how many times the playlist should be watched, and `num_videos_to_watch` determines how many videos should be watched in each iteration.

Please, use this code responsibly and ensure compliance with YouTube's terms of service. Automated YouTube interactions might lead to account restrictions or other consequences.


To run the Docker container in the background (detached mode), you can use the `-d` flag when running the `docker run` command. This flag instructs Docker to run the container in the background, and you will get back the command prompt immediately after starting the container.

Here's how to run the Docker container in the background:

1. Rebuild the Docker image (if you haven't already):

```bash
docker build -t youtube_agent .
```

2. Run the Docker container in detached mode (`-d` flag) and add the `--restart always` option to ensure the container restarts automatically:

```bash
docker run -d --name youtube_agent_container --restart always youtube_agent
```

The `-d` flag tells Docker to run the container in the background, and the `--restart always` option ensures that the container restarts automatically if it stops for any reason.

Now, the Docker container will run in the background, and you will get back the command prompt immediately. The YouTube agent will keep watching the videos continuously, and the container will restart automatically if it stops or crashes. You can view the logs of the container using the `docker logs` command:

```bash
docker logs youtube_agent_container
```

This will display the verbose logs that we added to the script, showing the progress of the agent as it watches the videos.

To stop the container, you can use the `docker stop` command:

```bash
docker stop youtube_agent_container
```

And to start it again:

```bash
docker start youtube_agent_container
```

With this setup, the Docker container will run the YouTube agent continuously in the background, ensuring that your videos are being watched as intended.

--- 

## Troubleshooting

### urllib3: ValueError: Timeout value connect was <object object at 0x7efe5adb9aa0>, but it must be an int, float or None

A new version 2.0.2 of urllib3 was released on May 4, 2023, which can be seen here: urllib3 2.0.2 - Release history

As my job installs the Python libraries in the beginning of the job using pip in a virtual Python environment, it started installing the latest version of urllib3 which had some issues. So, it is looks an upstream issue.

I fixed it by adding urllib3>=1.26.15,<2 in my requirements.txt file.