# Automated Web Scraping and Data Visualization
#### Video Demo: <URL HERE>
#### Description:
This project focuses on automated web scraping, utilizing Selenium to gather data from various sources and presenting the data through a user-friendly interface using PyQt5. The project combines data from Amazon and Flipkart to provide comprehensive product statistics and extracts information from YouTube videos to display views, titles, and descriptions. The data is then visualized using Matplotlib for better insights.

## Project Overview
Automated data collection and analysis are crucial in today's data-driven world. This project aims to simplify the process of gathering and visualizing data from popular e-commerce platforms and YouTube. The application serves as a powerful tool for users looking to compare product statistics or analyze YouTube video metrics.

## Features
1. **Data Extraction from Amazon and Flipkart**:
    - Uses Selenium to visit product pages on Amazon and Flipkart.
    - Extracts key product information such as price, ratings, reviews, and more.
    - Combines and displays the data for easy comparison.

2. **YouTube Video Data Extraction**:
    - Uses Selenium to visit YouTube video pages.
    - Extracts video title, views, description, and other relevant metrics.
  
3. **Data Visualization**:
    - Utilizes Matplotlib to create visual representations of the collected data.
    - Generates graphs and charts to help users understand and analyze the data effectively.

4. **User Interface**:
    - Built with PyQt5 to provide a smooth and interactive user experience.
    - Allows users to input URLs for the data extraction and view results within the application.

## File Descriptions
- `pyqttrial.py`: The main script that initializes the application and handles user interactions.
- `scraper.py`: Contains the web scraping logic using Selenium. Includes functions for extracting data from Amazon, Flipkart, and YouTube.
- `visualizer.py`: Handles data visualization using Matplotlib. Includes functions for creating different types of charts and graphs.
- `ui_main.py`: Defines the PyQt5 user interface layout and components.
- `config.py`: Configuration file containing settings and parameters for the web scraping and visualization processes.

## Design Choices
### Web Scraping with Selenium
Selenium was chosen for its ability to interact with dynamic web pages, which is essential for scraping modern websites like Amazon, Flipkart, and YouTube. Other libraries like BeautifulSoup were considered but were not sufficient for handling the JavaScript-heavy content on these platforms.

### Data Visualization with Matplotlib
Matplotlib was selected for its extensive capabilities and flexibility in creating a wide range of visualizations. While libraries like Seaborn and Plotly offer enhanced aesthetics, Matplotlib provides the necessary control and customization options for this project.

### User Interface with PyQt5
PyQt5 was chosen to create a desktop application that offers a seamless and interactive user experience. Other options like Tkinter and Kivy were considered, but PyQt5's extensive documentation and features made it the preferred choice.

## Installation and Setup
1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```bash
    python main.py
    ```

## Usage
1. Open the application.
2. Input the URL of the Amazon or Flipkart product you want to compare.
3. Input the URL of the YouTube video to extract data.
4. Click the "Scrape" button to initiate the data extraction.
5. View the combined statistics and visualizations within the application.

## Future Enhancements
- **Support for Additional Platforms**: Extend the scraping capabilities to include other e-commerce and video platforms.
- **Enhanced Visualization Options**: Integrate more advanced visualization libraries like Plotly for interactive charts.
- **Data Export**: Add functionality to export the scraped data and visualizations to CSV or PDF formats.

## Conclusion
This project demonstrates the power of automated web scraping and data visualization in providing valuable insights from multiple sources. The use of Selenium, Matplotlib, and PyQt5 creates a robust and user-friendly tool for data analysis.

Feel free to reach out for any questions or suggestions regarding this project.






