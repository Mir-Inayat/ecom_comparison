import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QDialog, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QWidget, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from ytscrape import get_video_details  # Assuming this function is available and returns video details as a dictionary
from scrape_all import scrape_amazon, scrape_flipkart
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

class ScrapingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scraping Dashboard")
        self.setGeometry(100, 100, 1000, 800)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.header = QLabel("Scraping Dashboard", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: black; padding: 20px;")
        self.layout.addWidget(self.header)

        self.ecommerce_btn = QPushButton("Ecommerce Scraping", self)
        self.ecommerce_btn.setStyleSheet("font-size: 14px; background-color: #007BFF; color: white; padding: 10px;")
        self.ecommerce_btn.clicked.connect(self.ecommerce_scraping)
        self.layout.addWidget(self.ecommerce_btn)

        self.youtube_btn = QPushButton("YouTube Scraping", self)
        self.youtube_btn.setStyleSheet("font-size: 14px; background-color: #007BFF; color: white; padding: 10px;")
        self.youtube_btn.clicked.connect(self.youtube_scraping)
        self.layout.addWidget(self.youtube_btn)

        self.results_label = QLabel("Scraping Results", self)
        self.results_label.setAlignment(Qt.AlignCenter)
        self.results_label.setStyleSheet("font-size: 18px; color: white; background-color: black; padding: 10px;")
        self.results_label.hide()
        self.layout.addWidget(self.results_label)

        self.results_text = QTextEdit(self)
        self.results_text.setStyleSheet("font-size: 12px; background-color: black; color: white;")
        self.results_text.hide()
        self.layout.addWidget(self.results_text)

        self.results_table = QTableWidget(self)
        self.results_table.hide()
        self.layout.addWidget(self.results_table)

        self.plot_label = QLabel(self)
        self.plot_label.setAlignment(Qt.AlignCenter)
        self.plot_label.hide()
        self.layout.addWidget(self.plot_label)

    def display_results(self, data, img_path=None):
        self.results_label.show()
        if isinstance(data, str):
            self.results_text.show()
            self.results_text.clear()
            self.results_text.setText(data)
            self.results_table.hide()
        elif isinstance(data, pd.DataFrame):
            self.results_text.hide()
            self.results_table.show()
            self.results_table.setRowCount(len(data))
            self.results_table.setColumnCount(len(data.columns))
            self.results_table.setHorizontalHeaderLabels(data.columns)
            for i, row in data.iterrows():
                for j, value in enumerate(row):
                    self.results_table.setItem(i, j, QTableWidgetItem(str(value)))

        if img_path:
            pixmap = QPixmap(img_path)
            self.plot_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio))
            self.plot_label.show()
        else:
            self.plot_label.hide()

    def ecommerce_scraping(self):
        product, ok = QInputDialog.getText(self, "Input", "Enter the product you want to compare:")
        if ok and product:
            try:
                self.search_af(product)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def search_af(self, product):
        try:
            amazon_df = scrape_amazon(product)
            flipkart_df = scrape_flipkart(product)

            amazon_avg_price = amazon_df['Price'].mean()
            flipkart_avg_price = flipkart_df['Price'].mean()
            price_comparison = f"Average Price on Amazon: {amazon_avg_price:.2f}\nAverage Price on Flipkart: {flipkart_avg_price:.2f}\n"

            amazon_avg_rating = amazon_df['Rating'].mean()
            flipkart_avg_rating = flipkart_df['Rating'].mean()
            rating_comparison = f"Average Rating on Amazon: {amazon_avg_rating:.2f}\nAverage Rating on Flipkart: {flipkart_avg_rating:.2f}\n"

            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            sns.histplot(amazon_df['Price'], bins=20, color='blue', label='Amazon', kde=True)
            sns.histplot(flipkart_df['Price'], bins=20, color='orange', label='Flipkart', kde=True)
            plt.title('Price Distribution Comparison')
            plt.xlabel('Price')
            plt.ylabel('Frequency')
            plt.legend()
            plt.grid(True)

            plt.subplot(1, 2, 2)
            sns.histplot(amazon_df['Rating'], bins=5, color='blue', label='Amazon', kde=True)
            sns.histplot(flipkart_df['Rating'], bins=5, color='orange', label='Flipkart', kde=True)
            plt.title('Rating Distribution Comparison')
            plt.xlabel('Rating')
            plt.ylabel('Frequency')
            plt.legend()
            plt.grid(True)

            image_path = os.path.join(os.getcwd(), "ecommerce_comparison.png")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()

            comparison_results = f"{price_comparison}\n{rating_comparison}"
            self.display_results(comparison_results, img_path=image_path)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while scraping ecommerce data: {e}")

    def get_youtube_video_urls(self, search_query):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        try:
            driver.get("https://www.youtube.com")
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(10)
            video_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.title-and-badge.style-scope.ytd-video-renderer"))
            )
            video_urls = [video.find_element(By.TAG_NAME, 'a').get_attribute("href") for video in video_elements]
        except Exception as e:
            print(f"An error occurred while fetching video URLs: {e}")
            video_urls = []
        finally:
            driver.quit()
        return video_urls

    def youtube_scraping(self):
        query, ok = QInputDialog.getText(self, "Input", "What do you want to search for on YouTube:")
        if not ok or not query:
            return

        urls = self.get_youtube_video_urls(query)

        video_data = []
        for url in urls:
            try:
                details = get_video_details(url)
                if details:  # Ensure details are not None
                    video_data.append(details)
                else:
                    print(f"Details for URL {url} are None.")
            except Exception as e:
                print(f"An error occurred while getting details for {url}: {e}")

        if video_data:
            df = pd.DataFrame(video_data)
            csv_file = "youtube_videos.csv"
            df.to_csv(csv_file, index=False)
            self.display_results(df)
        else:
            self.display_results("No video details were extracted.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrapingApp()
    window.show()
    sys.exit(app.exec_())
