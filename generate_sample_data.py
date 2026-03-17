import os
import pandas as pd

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Sample Home Prices CSV
home_prices = pd.DataFrame({
    "RegionName": ["Austin", "Boston", "Chicago", "Denver", "Miami",
                   "New York", "Philadelphia", "San Francisco", "Seattle", "Washington"],
    "StateName": ["TX", "MA", "IL", "CO", "FL", "NY", "PA", "CA", "WA", "DC"],
    "2026-02-01": [450000, 700000, 350000, 500000, 400000, 900000, 300000, 1200000, 650000, 600000]
})
home_prices.to_csv("data/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv", index=False)

# Sample Rent Prices CSV
rent_prices = pd.DataFrame({
    "RegionName": ["Austin", "Boston", "Chicago", "Denver", "Miami",
                   "New York", "Philadelphia", "San Francisco", "Seattle", "Washington"],
    "2026-02-01": [2200, 3000, 1800, 2500, 2000, 4000, 1700, 4500, 3200, 2900]
})
rent_prices.to_csv("data/Metro_zori_uc_sfrcondomfr_sm_month.csv", index=False)

print("Sample CSVs created in the 'data/' folder.")
