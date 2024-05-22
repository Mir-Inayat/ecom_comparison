import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Scrape data from Amazon and Flipkart
from scrape_all import scrape_amazon, scrape_flipkart
s=input("What do you want to compare: ")

amazon_df = scrape_amazon(s)
flipkart_df = scrape_flipkart(s)

# Combine the two DataFrames
combined_df = pd.concat([amazon_df, flipkart_df], keys=["Amazon", "Flipkart"])

# Reset the index
combined_df = combined_df.reset_index(level=1, drop=True)
combined_df = combined_df.reset_index()

# Add a column for the source
combined_df["Source"] = np.where(combined_df.index < len(amazon_df), "Amazon", "Flipkart")

# Convert non-numeric values in the Rating column to NaN
combined_df["Rating"] = pd.to_numeric(combined_df["Rating"], errors='coerce')

# Convert the "Price" column to numeric type
combined_df["Price"] = pd.to_numeric(combined_df["Price"], errors='coerce')

# Drop rows with NaN values in the "Price" column
combined_df = combined_df.dropna(subset=["Price"])

# Visualize the data
plt.figure(figsize=(10, 6))

# Plot the distribution of ratings
plt.subplot(1, 2, 1)
combined_df.boxplot(column="Rating", by="Source")
plt.title("Distribution of Ratings")
plt.xticks(rotation=45)

# Plot the distribution of prices
plt.subplot(1, 2, 2)
combined_df.boxplot(column="Price", by="Source")
plt.title("Distribution of Prices")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
