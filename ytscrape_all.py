import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
from ytscrape import get_video_details  # Assuming this function is available and returns video details as a dictionary

# Function to search YouTube and extract video URLs
def get_youtube_video_urls(search_query):
    # Set up the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Open YouTube
        driver.get("https://www.youtube.com")

        # Find the search bar and enter the search query
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the results to load,
        # adjust according to network speed
        time.sleep(10)

        # Extract video URLs
        video_elements = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
        video_urls = [video.get_attribute("href") for video in video_elements if video.get_attribute("href")]
    finally:
        # Close the WebDriver
        driver.quit()

    return video_urls

# Function to store data in MongoDB
def store_in_mongo(df, db_name, collection_name):
    try:
        client = MongoClient('localhost', 27017)  # Connect to MongoDB (make sure MongoDB is running)
        db = client[db_name]
        collection = db[collection_name]
        collection.insert_many(df.to_dict('records'))
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")

# Example usage
if __name__ == "__main__":
    #query = "Python programming"
    query = input("What do you want to search for : ")
    urls = get_youtube_video_urls(query)
    
    video_data = []
    for url in urls:
        try:
            details = get_video_details(url)
            video_data.append(details)
        except Exception as e:
            print(f"An error occurred while getting details for {url}: {e}")

    if video_data:
        # Create a DataFrame
        df = pd.DataFrame(video_data)

        # Save DataFrame to CSV
        csv_file = "youtube_videos.csv"
        df.to_csv(csv_file, index=False)
        
        # Store data in MongoDB
        store_in_mongo(df, 'youtube_db', 'videos')

        # Display the DataFrame
        print(df)
    else:
        print("No video details were extracted.")




