from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Function to search YouTube and extract video URLs
def get_youtube_video_urls(search_query):
    # Open YouTube
    driver.get("https://www.youtube.com")

    # Find the search bar and enter the search query
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(3)

    # Extract video URLs
    video_elements = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    video_urls = [video.get_attribute("href") for video in video_elements if video.get_attribute("href")]

    return video_urls

# Example usage
if __name__ == "__main__":
    query = "Python programming"
    urls = get_youtube_video_urls(query)
    for url in urls:
        print(url)

    # Close the WebDriver
    driver.quit()
