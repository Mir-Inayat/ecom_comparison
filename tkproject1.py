import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
from ytscrape import get_video_details  # Assuming this function is available and returns video details as a dictionary
from scrape_all import scrape_amazon, scrape_flipkart
import matplotlib.pyplot as plt
import seaborn as sns

class ScrapingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scraping Dashboard")
        self.geometry("800x600")  # Increased the window size for better text display
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Scraping Dashboard", font=("Arial", 24)).pack(pady=20)

        self.ecommerce_btn = tk.Button(self, text="Ecommerce Scraping", command=self.ecommerce_scraping)
        self.ecommerce_btn.pack(pady=10)

        self.youtube_btn = tk.Button(self, text="YouTube Scraping", command=self.youtube_scraping)
        self.youtube_btn.pack(pady=10)

        self.results_label = tk.Label(self, text="Scraping Results", font=("Arial", 18))
        self.results_label.pack(pady=10)
        self.results_label.pack_forget()

        self.results_text = tk.Text(self, height=20, width=100, wrap=tk.WORD)
        self.results_text.pack(pady=10)
        self.results_text.pack_forget()

        self.plot_label = tk.Label(self)
        self.plot_label.pack(pady=10)
        self.plot_label.pack_forget()

    def display_results(self, data, img=None):
        self.results_label.pack()
        self.results_text.pack()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, data)

        if img:
            self.plot_label.pack()
            self.plot_label.config(image=img)
            self.plot_label.image = img

    def ecommerce_scraping(self):
        product = simpledialog.askstring("Input", "Enter the product you want to compare:")
        if product:
            try:
                # Call search_af function to compare prices and ratings
                self.search_af(product)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def search_af(self, product):
        amazon_df = scrape_amazon(product)
        flipkart_df = scrape_flipkart(product)

        # Price comparison
        amazon_avg_price = amazon_df['Price'].mean()
        flipkart_avg_price = flipkart_df['Price'].mean()

        price_comparison = f"Average Price on Amazon: {amazon_avg_price}\nAverage Price on Flipkart: {flipkart_avg_price}\n"

        # Rating comparison
        amazon_avg_rating = amazon_df['Rating'].mean()
        flipkart_avg_rating = flipkart_df['Rating'].mean()

        rating_comparison = f"Average Rating on Amazon: {amazon_avg_rating}\nAverage Rating on Flipkart: {flipkart_avg_rating}\n"

        # Visualize data
        plt.figure(figsize=(12, 6))

        # Price distribution comparison
        plt.subplot(1, 2, 1)
        sns.histplot(amazon_df['Price'], bins=20, color='blue', label='Amazon', kde=True)
        sns.histplot(flipkart_df['Price'], bins=20, color='orange', label='Flipkart', kde=True)
        plt.title('Price Distribution Comparison')
        plt.xlabel('Price')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)

        # Rating distribution comparison
        plt.subplot(1, 2, 2)
        sns.histplot(amazon_df['Rating'], bins=5, color='blue', label='Amazon', kde=True)
        sns.histplot(flipkart_df['Rating'], bins=5, color='orange', label='Flipkart', kde=True)
        plt.title('Rating Distribution Comparison')
        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)

        # Specify the full path where you want to save the image file
        image_path = os.path.join(os.getcwd(), "ecommerce_comparison.png")

        plt.tight_layout()
        plt.savefig(image_path)  # Save the plot as an image using the full path
        plt.close()  # Close the

        # Combine the comparison results
        comparison_results = f"{price_comparison}\n{rating_comparison}"

        # Display the comparison results and the plot in the Tkinter GUI
        self.display_results(comparison_results, img=image_path)

    def get_youtube_video_urls(self, search_query):
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
            time.sleep(5)

            # Extract video URLs
            video_elements = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
            video_urls = [video.get_attribute("href") for video in video_elements if video.get_attribute("href")]
        finally:
            # Close the WebDriver
            driver.quit()

        return video_urls

    def store_in_mongo(self, df, db_name, collection_name):
        try:
            client = MongoClient('localhost', 27017)  # Connect to MongoDB (make sure MongoDB is running)
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_many(df.to_dict('records'))
        except Exception as e:
            print(f"An error occurred while connecting to MongoDB: {e}")

    def youtube_scraping(self):
        query = simpledialog.askstring("Input", "What do you want to search for on YouTube:")
        if not query:
            return
        
        urls = self.get_youtube_video_urls(query)
        
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
            self.store_in_mongo(df, 'youtube_db', 'videos')

            # Display the DataFrame
            self.display_results(df.to_string())
        else:
            self.display_results("No video details were extracted.")

if __name__ == "__main__":
    app = ScrapingApp()
    app.mainloop()
