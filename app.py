# %%
import pandas as pd
import os
import streamlit as st
os.makedirs("data", exist_ok=True)

home_csv = "data/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
rent_csv = "data/Metro_zori_uc_sfrcondomfr_sm_month.csv"

# Generate sample data if files do not exist
if not os.path.isfile(home_csv) or not os.path.isfile(rent_csv):
    st.warning("Zillow data not found. Generating sample data for demo purposes...")

    # Sample Home Prices CSV
    home_prices = pd.DataFrame({
        "RegionName": ["Austin", "Boston", "Chicago", "Denver", "Miami",
                       "New York", "Philadelphia", "San Francisco", "Seattle", "Washington"],
        "StateName": ["TX", "MA", "IL", "CO", "FL", "NY", "PA", "CA", "WA", "DC"],
        "2026-02-01": [450000, 700000, 350000, 500000, 400000, 900000, 300000, 1200000, 650000, 600000]
    })
    home_prices.to_csv(home_csv, index=False)

    # Sample Rent Prices CSV
    rent_prices = pd.DataFrame({
        "RegionName": ["Austin", "Boston", "Chicago", "Denver", "Miami",
                       "New York", "Philadelphia", "San Francisco", "Seattle", "Washington"],
        "2026-02-01": [2200, 3000, 1800, 2500, 2000, 4000, 1700, 4500, 3200, 2900]
    })
    rent_prices.to_csv(rent_csv, index=False)

# Home prices
df = pd.read_csv(home_csv)
df.head()
df.info()

# %%
latest_month = df.columns[-1]

df = df[["RegionName", "StateName", latest_month]]

df.columns = ["City", "State", "Home_Price"]

df.head()

# %%
# Rent
rent_df = pd.read_csv(rent_csv)
latest_rent_month = rent_df.columns[-1]
rent_df = rent_df[["RegionName", latest_rent_month]]
rent_df.columns = ["City", "Rent_Price"]

# Merge
merged = pd.merge(df, rent_df, on = "City")
merged.head()

# %%
# Model
# Price to Rent Ratio
merged["Rent_to_Price_Ratio"] = merged["Rent_Price"] / (merged["Home_Price"] * 12)

# Rent Yield %
merged["Rent_Yield"] = merged["Rent_Price"] / merged["Home_Price"] * 100

# %%
# Normalized values
merged["Normalized_Rent_to_Price_Ratio"] = (merged["Rent_to_Price_Ratio"] - merged["Rent_to_Price_Ratio"].min()) / (merged["Rent_to_Price_Ratio"].max() - merged["Rent_to_Price_Ratio"].min())
merged["Normalized_Rent_Yield"] = (merged["Rent_Yield"] - merged["Rent_Yield"].min()) / (merged["Rent_Yield"].max() - merged["Rent_Yield"].min())

# Investment score, weighted sum
merged["Investment_Score"] = 0.4 * merged["Normalized_Rent_to_Price_Ratio"] + 0.6 * merged["Normalized_Rent_Yield"]

# Investment score sorted by score descending
merged_sorted = merged.sort_values(by = "Investment_Score", ascending = False)

# %%
print(merged_sorted[["City", "State", "Home_Price", "Rent_Price", "Rent_to_Price_Ratio", "Rent_Yield", "Investment_Score"]].head(20))

# %%
import matplotlib.pyplot as plt

# Bar chart
plt.figure(figsize = (12, 6))
plt.bar(merged_sorted["City"].head(20), merged_sorted["Investment_Score"].head(20), color = "skyblue")
plt.xticks(rotation = 90)
plt.xlabel("City")
plt.ylabel("Investment Score")
plt.title("Top 20 Cities by Real Estate Investment Score")
plt.tight_layout()
plt.show()


# %%
import streamlit as st

st.title("Real Estate Investment Analysis")

# User input: cities
selected_cities = st.multiselect("Select Cities", merged_sorted["City"].unique(), default = merged_sorted["City"].head(10).tolist())

# Filter data
filtered_data = merged_sorted[merged_sorted["City"].isin(selected_cities)].copy()

st.dataframe(filtered_data[["City", "State", "Home_Price", "Rent_Price", "Rent_to_Price_Ratio", "Rent_Yield", "Investment_Score"]])

# Bar chart
st.bar_chart(filtered_data.set_index("City")["Investment_Score"])

# %%
# Popular Cities according to Zillow
popular_cities = pd.DataFrame({
    "City": ["Hartford, CT", "Buffalo, NY", "New York, NY", "Providence, RI", "San Jose, CA", "Philadelphia, PA", "Boston, MA",
             "Los Angeles, CA", "Richmond, VA", "Milwaukee, WI" ],
    "Source_Rank": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
})

comparison = pd.merge(popular_cities, merged_sorted, on = "City", how = "left")
st.write("Comparison of Popular Cities Ranked on Zillow")
st.dataframe(comparison[["City", "Investment_Score", "Source_Rank"]])

# %%
st.markdown("""
## How the Model Works

The **Investment Score** is calculated as a weighted sum of:

- **Normalized Rent-to-Price Ratio**
- **Normalized Rent Yield**

Higher scores indicate cities where rental income is high relative to home price.

### Zillow Comparison
The table below compares our top 10 cities to Zillow's rankings.
""")


