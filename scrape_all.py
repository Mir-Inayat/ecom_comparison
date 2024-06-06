import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

def scrape_amazon(item):
    # Set up Selenium
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Navigate to Amazon
    driver.get("https://www.amazon.in/")

    # Find the search input field
    search_input = driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")

    # Enter the search query (replace 'mobile phone' with your desired search query)
    search_input.send_keys(item)

    # Press Enter to perform the search
    search_input.send_keys(Keys.ENTER)

    # Find elements containing product names, prices, and ratings
    product_elements = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    # Initialize lists to store data
    names = []
    prices = []
    ratings = []

    # Extract product information
    for product_element in product_elements:
        # Extract product name
        product_name_element = product_element.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']")
        product_name = product_name_element.text
        names.append(product_name)

        # Extract product price
        try:
            product_price_element = product_element.find_element(By.XPATH, ".//span[@class='a-price-whole']")
            product_price = product_price_element.text
        except:
            product_price = "0"
        prices.append(float(product_price.replace(',', '')))

        # Extract product rating
        try:
            product_rating_element = product_element.find_element(By.XPATH, ".//span[@class='a-icon-alt']")
            product_rating = product_rating_element.get_attribute("innerHTML")
            product_rating = product_rating[:3]
        except:
            product_rating = "0"
        ratings.append(float(product_rating))

    # Close the driver
    driver.quit()

    # Create DataFrame
    data = {
        "Name": names,
        "Price": prices,
        "Rating": ratings
    }
    df = pd.DataFrame(data)
    # Save DataFrame to CSV
    df.to_csv('amazon.csv', index=False)

    # Return DataFrame
    return df

def scrape_flipkart(item):
    # Set up Selenium
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Navigate to Flipkart
    driver.get("https://www.flipkart.com/")

    # Find the search input field
    search_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div/div[1]/div[1]/header/div[1]/div[2]/form/div/div/input")

    # Enter the search query
    search_input.send_keys(item)

    # Press Enter to perform the search
    search_input.send_keys(Keys.ENTER)

    # Find elements containing product names, prices, and ratings
    product_elements = driver.find_elements(By.XPATH, "//div[@class='tUxRFH']")

    # Initialize lists to store data
    names = []
    prices = []
    ratings = []

    # Extract product information
    for product_element in product_elements:
        # Extract product name
        product_name_element = product_element.find_element(By.CSS_SELECTOR, "div.KzDlHZ")
        product_name = product_name_element.text
        names.append(product_name)

        # Extract product price
        product_price_element = product_element.find_element(By.CSS_SELECTOR, "div._4b5DiR")
        product_price = product_price_element.text
        prices.append(float(product_price.replace('₹', '').replace(',', '')))

        # Extract product rating
        product_rating_element = product_element.find_element(By.CSS_SELECTOR, "div.XQDdHH")
        product_rating = product_rating_element.text
        ratings.append(float(product_rating))

    # Close the driver
    driver.quit()

    # Create DataFrame
    data = {"Name": names, "Price": prices, "Rating": ratings}
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv('flipkart.csv', index=False)

    # Return DataFrame
    return df

def main():
    # Call the scrape_amazon function to search for mobile phones on Amazon and extract product information
    amazon_df = scrape_amazon("mobile")
    # Call the scrape_amazon function to search for mobile phones on Flipkart and extract product information
    flipkart_df = scrape_flipkart("mobile")
    # Print the DataFrame
    print(amazon_df)
    # Print the DataFrame
    print(flipkart_df)
if __name__=="__main__":
    main()